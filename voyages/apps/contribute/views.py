from __future__ import absolute_import, print_function, unicode_literals

import gc
import json
import os
import re
import tempfile
import traceback
from builtins import range, str
from itertools import chain

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import connection, transaction
from django.db.models.fields import Field
from django.http import (Http404, HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import get_object_or_404, render
from django.utils.html import escape
from django.utils.translation import ugettext as u_
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# Create your views here.
from future import standard_library
import six
import _thread

from voyages.apps.common.views import get_ordered_places
from voyages.apps.contribute.forms import (ContributionVoyageSelectionForm,
                                           InterimVoyageForm)
from voyages.apps.contribute.models import (ContributionStatus,
                                            DeleteVoyageContribution,
                                            EditorVoyageContribution,
                                            EditVoyageContribution,
                                            InterimPreExistingSource,
                                            InterimSlaveNumber, InterimVoyage,
                                            MergeVoyagesContribution,
                                            NewVoyageContribution,
                                            ReviewRequest,
                                            ReviewRequestDecision,
                                            ReviewRequestResponse,
                                            ReviewVoyageContribution, User,
                                            get_all_new_sources_for_interim,
                                            get_contribution,
                                            get_contribution_from_id,
                                            source_type_dict)
from voyages.apps.contribute.publication import (
    export_contributions, export_from_voyages, full_contribution_id,
    get_csv_writer, get_filtered_contributions, get_header_csv_text,
    publish_accepted_contributions, safe_writerow)
from voyages.apps.voyage.cache import VoyageCache
from voyages.apps.voyage.forms import VoyagesSourcesAdminForm
from voyages.apps.voyage.models import (Voyage, VoyageDataset, VoyageDates,
                                        VoyageShipOwnerConnection,
                                        VoyageSources, VoyageSourcesConnection,
                                        VoyageSourcesType)
from voyages.apps.voyage.views import voyage_variables_data

from . import imputed
from .forms import legal_terms_paragraph, legal_terms_title

standard_library.install_aliases()

number_prefix = 'interim_slave_number_'


def index(request):
    """
    Handles the redirection when user attempts to login
    Display the user index page if the user is already authenticated
    Or return to the login page if the user has not logged in yet
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account_login'))
    filter_args = {
        'contributor': request.user,
        'status__lte': ContributionStatus.committed
    }
    contributions = get_filtered_contributions(filter_args)
    review_requests = ReviewRequest.objects.filter(
        suggested_reviewer=request.user,
        response__lte=1,
        archived=False,
        final_decision=0)
    return render(request, "contribute/index.html", {
        'contributions': contributions,
        'review_requests': review_requests
    })


def legal(request):
    return render(request, 'contribute/legal.html', {
        'title': legal_terms_title,
        'paragraph': legal_terms_paragraph
    })


def get_summary(v):
    dates = v.voyage_dates
    return {
        'voyage_id':
            v.voyage_id,
        'captain':
            ', '.join([c.name for c in v.voyage_captain.all()]),
        'ship':
            v.voyage_ship.ship_name,
        'year_arrived':
            dates.get_date_year(
                dates.first_dis_of_slaves
            ) or dates.get_date_year(dates.imp_arrival_at_port_of_dis)
    }


def set_isolation_serializable():
    cursor = connection.cursor()
    cursor.execute('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE')


@csrf_exempt
def get_voyage_by_id(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'})
    voyage_id = request.POST.get('voyage_id')
    if voyage_id is None:
        return JsonResponse({'error': 'Missing voyage_id field in POST'})
    voyage_id = int(voyage_id)
    v = Voyage.all_dataset_objects.filter(voyage_id=voyage_id).first()
    if v is None:
        return JsonResponse({
            'error': 'No voyage found with voyage_id = ' + str(voyage_id)
        })
    summary = get_summary(v)
    # Check whether the voyage already has an open contribution.
    active_statuses = ContributionStatus.active_statuses
    regex = '(^' + str(voyage_id) + '|,' + str(voyage_id) + ')(,|$)'
    is_blocked = any([
        EditVoyageContribution.objects.filter(
            edited_voyage_id=voyage_id,
            status__in=active_statuses).count() > 0,
        MergeVoyagesContribution.objects.filter(
            merged_voyages_ids__iregex=regex,
            status__in=active_statuses).count() > 0,
        DeleteVoyageContribution.objects.filter(
            deleted_voyages_ids__iregex=regex,
            status__in=active_statuses).count() > 0
    ])
    summary['is_blocked'] = is_blocked
    return JsonResponse(summary)


@cache_page(24 * 60 * 60)
@csrf_exempt
def get_places(_):
    # retrieve list of places in the system.
    result = get_ordered_places()
    return JsonResponse(result, safe=False)


@login_required
def delete(request):
    if request.method != 'POST':
        form = ContributionVoyageSelectionForm()
        return render(request, 'contribute/delete.html', {
            'form': form,
            'voyage_selection': []
        })
    form = ContributionVoyageSelectionForm(data=request.POST)
    if not form.is_valid():
        ids = form.selected_voyages
        voyage_selection = [
            get_summary(v)
            for v in Voyage.all_dataset_objects.filter(voyage_id__in=ids)
        ]
        return render(request, 'contribute/delete.html', {
            'form': form,
            'voyage_selection': voyage_selection
        })
    ids = form.cleaned_data['ids']
    with transaction.atomic():
        contribution = DeleteVoyageContribution()
        contribution.contributor = request.user
        contribution.status = ContributionStatus.pending
        contribution.deleted_voyages_ids = ','.join(
            [str(x) for x in ids])
        contribution.notes = request.POST.get('notes')
        contribution.save()
    return HttpResponseRedirect(
        reverse('contribute:delete_review',
                kwargs={'contribution_id': contribution.pk}))


@login_required
def delete_review(request, contribution_id):
    contribution = get_object_or_404(DeleteVoyageContribution,
                                     pk=contribution_id)
    if request.user.pk != contribution.contributor.pk:
        return HttpResponseForbidden()
    if request.method != 'POST':
        return delete_review_render(
            request, contribution, False, 'contributor')
    action = request.POST.get('submit_val')
    if action == 'confirm':
        contribution.status = ContributionStatus.committed
        contribution.save()
        return HttpResponseRedirect(reverse('contribute:thanks'))
    if action == 'cancel':
        contribution.delete()
        return HttpResponseRedirect(reverse('contribute:index'))
    return HttpResponseBadRequest()


def delete_review_render(request, contribution, readonly, mode):
    ids = [int(pk) for pk in contribution.deleted_voyages_ids.split(',')]
    deleted_voyage_vars = [
        voyage_variables_data(voyage_id, mode == 'editor')[1]
        for voyage_id in ids
    ]
    review_request = None
    full_contrib_id = full_contribution_id('delete', contribution.pk)
    if mode != 'contributor':
        # Look for a review request for this delete contribution
        review_request = ReviewRequest.objects.filter(
            contribution_id=full_contrib_id, archived=False).first()
    return render(
        request, 'contribute/delete_review.html', {
            'deleted_voyage_vars': deleted_voyage_vars,
            'voyage_selection': ids,
            'readonly': readonly,
            'mode': mode,
            'review_request': review_request,
            'full_contrib_id': full_contrib_id
        })


@login_required
def edit(request):
    voyage_selection = []
    if request.method == 'POST':
        form = ContributionVoyageSelectionForm(data=request.POST, max_selection=1)
        if form.is_valid():
            ids = form.cleaned_data['ids']
            print(ids)
            with transaction.atomic():
                interim_voyage = InterimVoyage()
                interim_voyage.save()
                contribution = EditVoyageContribution()
                contribution.interim_voyage = interim_voyage
                contribution.contributor = request.user
                contribution.edited_voyage_id = ids[0]
                contribution.status = ContributionStatus.pending
                contribution.save()
                init_interim_voyage(interim_voyage, contribution)
            return HttpResponseRedirect(reverse(
                'contribute:interim', kwargs={'contribution_type': 'edit', 'contribution_id': contribution.pk}
            ))
        else:
            ids = form.selected_voyages
            voyage_selection = [get_summary(v) for v in Voyage.both_objects.filter(voyage_id=ids[0])] \
                if len(ids) != 0 else []
    else:
        form = ContributionVoyageSelectionForm(max_selection=1)
    return render(request, 'contribute/edit.html', {'form': form, 'voyage_selection': voyage_selection})


@login_required
def merge(request):
    if request.method != 'POST':
        form = ContributionVoyageSelectionForm(min_selection=2)
        return render(request, 'contribute/merge.html', {
            'form': form,
            'voyage_selection': []
        })
    form = ContributionVoyageSelectionForm(data=request.POST, min_selection=2)
    if not form.is_valid():
        ids = form.selected_voyages
        voyage_selection = [
            get_summary(v)
            for v in Voyage.all_dataset_objects.filter(voyage_id__in=ids)
        ]
        return render(request, 'contribute/merge.html', {
            'form': form,
            'voyage_selection': voyage_selection
        })
    ids = form.cleaned_data['ids']
    with transaction.atomic():
        interim_voyage = InterimVoyage()
        interim_voyage.save()
        contribution = MergeVoyagesContribution()
        contribution.interim_voyage = interim_voyage
        contribution.contributor = request.user
        contribution.merged_voyages_ids = ','.join(
            [str(x) for x in ids])
        contribution.status = ContributionStatus.pending
        contribution.save()
        init_interim_voyage(interim_voyage, contribution)
    return HttpResponseRedirect(
        reverse('contribute:interim',
                kwargs={
                    'contribution_type': 'merge',
                    'contribution_id': contribution.pk
                }))


def interim_source_model(src_type):
    result = source_type_dict.get(src_type)
    if result is None:
        raise Exception('Unrecognized source type: ' + src_type)
    return result


def create_source(source_values, interim_voyage):
    model = interim_source_model(source_values['type'])
    source = model()
    for k, v in list(source_values.items()):
        if v == '':
            continue
        if hasattr(source, k):
            setattr(source, k, v)
    source.interim_voyage = interim_voyage
    try:
        source.pk = int(source_values['pk'])
    except Exception:
        pass
    if source.created_voyage_sources:
        if not source.source_ref_text or not source.source_ref_text.startswith(
                source.created_voyage_sources.short_ref):
            raise Exception(
                'Invalid interim source: the text reference must have as '
                'prefix the short reference of the Source'
            )
    return source


interim_new_source_types = list(source_type_dict.values())


def interim_main(request, contribution, interim):
    """
    The reusable part of the interim form handling.
    This function should be used in the views targeted at
    contributor, reviewer, and editor.
    :param request: the request which may contain interim form POST data.
    :param contribution: the contribution object, which may be a review.
    :param interim: the interim voyage data.
    :return: (Boolean b, numbers, form, source_pks)
    First entry of tuple is True if GET request or valid POST, False otherwise.
    Numbers: dictionary of slave numbers
    Form: the interim form.
    Source pks: the primary key of the source references
    """
    result = True
    src_pks = {}
    if request.method != 'POST':
        numbers = {
            number_prefix + n.var_name: n.number
            for n in interim.slave_numbers.all()
        }
        form = InterimVoyageForm(instance=interim)
        return result, form, numbers, src_pks
    form = InterimVoyageForm(request.POST, instance=interim)
    prefix = number_prefix
    numbers = {
        k: float(v)
        for k, v in list(request.POST.items())
        if k.startswith(prefix) and v != ''
    }
    sources_post = request.POST.get('sources', '[]')
    sources = [(create_source(x, interim), x.get('__index'))
               for x in json.loads(sources_post)]
    result = form.is_valid()
    if not result:
        return result, form, numbers, src_pks
    with transaction.atomic():

        def del_children(child_model):
            child_model.objects.filter(
                interim_voyage__id=interim.pk).delete()

        for src_type in interim_new_source_types:
            del_children(src_type)

        del_children(InterimSlaveNumber)
        # Get pre-existing sources.
        for src in interim.pre_existing_sources.all():
            src.action = request.POST.get(
                'pre_existing_source_action_' + str(src.pk), 0)
            src.notes = escape(
                request.POST.get(
                    'pre_existing_source_notes_' + str(src.pk), ''))
            src.save()
        interim = form.save()
        # Additional form data.
        pesisted_fields = [
            'message_to_editor', 'reviewer_decision',
            'decision_message', 'editorial_decision',
            'created_voyage_id'
        ]
        pesisted_dict = {
            k: escape(request.POST[k])
            for k in pesisted_fields
            if k in request.POST
        }
        interim.persisted_form_data = json.dumps(
            pesisted_dict) if len(pesisted_dict) > 0 else None
        # Reparse notes safely.
        try:
            note_dict = {
                k: escape(v)
                for k, v in list(json.loads(interim.notes).items())
            }
        except Exception:
            note_dict = {'parse_error': interim.notes}
        interim.notes = json.dumps(note_dict)
        interim.save()
        contribution.notes = escape(
            request.POST.get('contribution_main_notes'))
        contribution.save()
        for (src, view_item_index) in sources:
            src.save()
            if view_item_index is not None:
                src_pks[view_item_index] = src.pk
        # Clear previous numbers and save new ones.
        for k, v in list(numbers.items()):
            number = InterimSlaveNumber()
            number.interim_voyage = interim
            number.var_name = k[len(prefix):]
            number.number = v
            number.save()
    return result, form, numbers, src_pks


@login_required
def interim(request, contribution_type, contribution_id):
    if contribution_type == 'delete':
        return HttpResponseRedirect(
            reverse('contribute:delete_review',
                    kwargs={'contribution_id': contribution_id}))

    contribution = get_contribution(contribution_type, contribution_id)
    if contribution is None:
        raise Http404
    if request.user.pk != contribution.contributor.pk:
        return HttpResponseForbidden()

    def redirect():
        return HttpResponseRedirect(
            reverse('contribute:interim_summary',
                    kwargs={
                        'contribution_type': contribution_type,
                        'contribution_id': contribution_id
                    }))

    if request.GET.get(
            'revert_to_pending'
    ) == 'true' and contribution.status <= ContributionStatus.committed:
        contribution.status = ContributionStatus.pending
        contribution.save()
    if contribution.status != ContributionStatus.pending:
        return redirect()
    interim = contribution.interim_voyage
    if request.method == 'POST' and request.POST.get('submit_val') == 'delete':
        with transaction.atomic():
            contribution.interim_voyage.delete()
            contribution.delete()
        return HttpResponseRedirect(reverse('contribute:index'))
    (valid, form, numbers, src_pks) = interim_main(request, contribution,
                                                   interim)
    if valid and request.method == 'POST' and (
            len(src_pks) > 0 or contribution_type != 'new'):
        return redirect()
    sources_post = None if request.method != 'POST' else request.POST.get(
        'sources')
    previous_data = contribution_related_data(contribution)
    return render(
        request, 'contribute/interim.html', {
            'form': form,
            'mode': 'contribute',
            'contribution': contribution,
            'numbers': numbers,
            'interim': interim,
            'sources_post': sources_post,
            'voyages_data': json.dumps(previous_data)
        })


def common_save_ajax(request, contribution):
    (valid, form, _, src_pks) = interim_main(request, contribution,
                                             contribution.interim_voyage)
    return JsonResponse({
        'valid': valid,
        'errors': form.errors,
        'src_pks': src_pks
    })


@login_required
@require_POST
def interim_save_ajax(request, contribution_type, contribution_id):
    contribution = get_contribution(contribution_type, contribution_id)
    if contribution is None:
        raise Http404
    if request.user.pk != contribution.contributor.pk:
        return HttpResponseForbidden()
    return common_save_ajax(request, contribution)


@login_required
@require_POST
def editorial_review_interim_save_ajax(request, editor_contribution_id):
    contribution = get_object_or_404(EditorVoyageContribution,
                                     pk=editor_contribution_id)
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    return common_save_ajax(request, contribution)


@login_required
@require_POST
def review_interim_save_ajax(request, reviewer_contribution_id):
    contribution = get_object_or_404(ReviewVoyageContribution,
                                     pk=reviewer_contribution_id)
    if request.user.pk != contribution.request.suggested_reviewer.pk:
        return HttpResponseForbidden()
    return common_save_ajax(request, contribution)


@login_required
def interim_commit(request, contribution_type, contribution_id):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    contribution = get_contribution(contribution_type, contribution_id)
    if contribution is None:
        raise Http404
    if any([request.user.pk != contribution.contributor.pk,
            contribution.status != ContributionStatus.pending]):
        return HttpResponseForbidden()
    contribution.status = ContributionStatus.committed
    contribution.save()
    return HttpResponseRedirect(reverse('contribute:thanks'))


@login_required()
def interim_summary(request,
                    contribution_type,
                    contribution_id,
                    mode='contribute'):
    contribution = get_contribution(contribution_type, contribution_id)
    if contribution is None:
        raise Http404
    if all([not request.user.is_superuser,
            not request.user.is_staff,
            request.user.pk != contribution.contributor.pk]):
        return HttpResponseForbidden()
    if contribution_type == 'delete':
        return delete_review_render(request, contribution, True, 'editor')
    numbers = {
        number_prefix + n.var_name: n.number
        for n in contribution.interim_voyage.slave_numbers.all()
    }
    form = InterimVoyageForm(instance=contribution.interim_voyage)
    previous_data = contribution_related_data(contribution)
    full_contrib_id = full_contribution_id(contribution_type, contribution_id)
    reqs = list(
        ReviewRequest.objects.filter(contribution_id=full_contrib_id,
                                     archived=False))
    if len(reqs) > 1:
        raise Exception(
            'Invalid state: more than one review request is active')
    review_request = reqs[0] if len(reqs) == 1 else None
    if review_request:
        review_contribution = review_request.review_contribution.first()
        if review_contribution and review_contribution.interim_voyage:
            previous_data[u_('Reviewer')] = interim_data(
                review_contribution.interim_voyage)
        editorial_contribution = review_request.editor_contribution.first()
        if editorial_contribution and editorial_contribution.interim_voyage:
            previous_data[u_('Editor')] = interim_data(
                editorial_contribution.interim_voyage)
    return render(
        request, 'contribute/interim_summary.html', {
            'contribution':
                contribution,
            'review_request':
                review_request,
            'full_contrib_id':
                full_contrib_id,
            'interim':
                contribution.interim_voyage,
            'mode':
                mode,
            'numbers':
                numbers,
            'form':
                form,
            'override_base':
                'print.html' if request.GET.get('printMode') else None,
            'user':
                request.user,
            'voyages_data':
                json.dumps(previous_data)
        })


@login_required
def new_voyage(request):
    interim_voyage = InterimVoyage()
    interim_voyage.save()
    contrib = NewVoyageContribution()
    contrib.contributor = request.user
    contrib.interim_voyage = interim_voyage
    contrib.status = ContributionStatus.pending
    contrib.save()
    return HttpResponseRedirect(
        reverse('contribute:interim',
                kwargs={
                    'contribution_type': 'new',
                    'contribution_id': contrib.pk
                }))


def init_interim_voyage(interim, contribution):
    # If this is a merger or edit, initialize fields when there is consensus.
    previous_data = contribution_related_data(contribution)
    if len(previous_data) > 0:
        values = list(previous_data.values())
        for k, v in list(values[0].items()):
            if v is None:
                continue
            equal = True
            for i in range(1, len(previous_data)):
                equal = v == values[i].get(k)
                if not equal:
                    break
            if equal:
                if k.startswith(number_prefix):
                    number = InterimSlaveNumber()
                    number.number = v
                    number.var_name = k[len(number_prefix):]
                    number.interim_voyage = interim
                    number.save()
                else:
                    if hasattr(interim, k + '_id'):
                        k += '_id'
                    setattr(interim, k, v)
    interim.save()
    # Fetch any existing sources, group them so that
    # references shared by more than one voyage are only
    # included once.
    related = contribution.get_related_voyages()
    source_to_voyage = {}
    for voyage in related:
        for conn in VoyageSourcesConnection.objects.filter(group=voyage):
            current = source_to_voyage.setdefault(conn.text_ref, [])
            current.append((voyage, conn))
    for tuples in list(source_to_voyage.values()):
        conn = tuples[0][1]
        ps = InterimPreExistingSource()
        ps.interim_voyage = interim
        ps.voyage_ids = ','.join([str(v.voyage_id) for (v, c) in tuples])
        ps.original_short_ref = conn.source.short_ref
        ps.original_ref = conn.text_ref
        ps.full_ref = conn.source.full_ref
        ps.save()


def contribution_related_data(contribution):
    previous_data = {}
    related = contribution.get_related_voyages()
    for voyage in related:
        previous_data[voyage.voyage_id] = voyage_to_dict(voyage)
    return previous_data


slave_number_var_map = {
    'SLADAFRI': 'slave_deaths_before_africa',
    'SLADVOY': 'slave_deaths_between_africa_america',
    'SLADAMER': 'slave_deaths_between_arrival_and_sale',
    'SLINTEND': 'num_slaves_intended_first_port',
    'SLINTEN2': 'num_slaves_intended_second_port',
    'NCAR13': 'num_slaves_carried_first_port',
    'NCAR15': 'num_slaves_carried_second_port',
    'NCAR17': 'num_slaves_carried_third_port',
    'TSLAVESP': 'total_num_slaves_purchased',
    'TSLAVESD': 'total_num_slaves_dep_last_slaving_port',
    'SLAARRIV': 'total_num_slaves_arr_first_port_embark',
    'SLAS32': 'num_slaves_disembark_first_place',
    'SLAS36': 'num_slaves_disembark_second_place',
    'SLAS39': 'num_slaves_disembark_third_place',
    'MEN1': 'num_men_embark_first_port_purchase',
    'WOMEN1': 'num_women_embark_first_port_purchase',
    'BOY1': 'num_boy_embark_first_port_purchase',
    'GIRL1': 'num_girl_embark_first_port_purchase',
    'ADULT1': 'num_adult_embark_first_port_purchase',
    'CHILD1': 'num_child_embark_first_port_purchase',
    'INFANT1': 'num_infant_embark_first_port_purchase',
    'MALE1': 'num_males_embark_first_port_purchase',
    'FEMALE1': 'num_females_embark_first_port_purchase',
    'MEN2': 'num_men_died_middle_passage',
    'WOMEN2': 'num_women_died_middle_passage',
    'BOY2': 'num_boy_died_middle_passage',
    'GIRL2': 'num_girl_died_middle_passage',
    'ADULT2': 'num_adult_died_middle_passage',
    'CHILD2': 'num_child_died_middle_passage',
    'INFANT2': 'num_infant_died_middle_passage',
    'MALE2': 'num_males_died_middle_passage',
    'FEMALE2': 'num_females_died_middle_passage',
    'MEN3': 'num_men_disembark_first_landing',
    'WOMEN3': 'num_women_disembark_first_landing',
    'BOY3': 'num_boy_disembark_first_landing',
    'GIRL3': 'num_girl_disembark_first_landing',
    'ADULT3': 'num_adult_disembark_first_landing',
    'CHILD3': 'num_child_disembark_first_landing',
    'INFANT3': 'num_infant_disembark_first_landing',
    'MALE3': 'num_males_disembark_first_landing',
    'FEMALE3': 'num_females_disembark_first_landing',
    'MEN4': 'num_men_embark_second_port_purchase',
    'WOMEN4': 'num_women_embark_second_port_purchase',
    'BOY4': 'num_boy_embark_second_port_purchase',
    'GIRL4': 'num_girl_embark_second_port_purchase',
    'ADULT4': 'num_adult_embark_second_port_purchase',
    'CHILD4': 'num_child_embark_second_port_purchase',
    'INFANT4': 'num_infant_embark_second_port_purchase',
    'MALE4': 'num_males_embark_second_port_purchase',
    'FEMALE4': 'num_females_embark_second_port_purchase',
    'MEN5': 'num_men_embark_third_port_purchase',
    'WOMEN5': 'num_women_embark_third_port_purchase',
    'BOY5': 'num_boy_embark_third_port_purchase',
    'GIRL5': 'num_girl_embark_third_port_purchase',
    'ADULT5': 'num_adult_embark_third_port_purchase',
    'CHILD5': 'num_child_embark_third_port_purchase',
    'INFANT5': 'num_infant_embark_third_port_purchase',
    'MALE5': 'num_males_embark_third_port_purchase',
    'FEMALE5': 'num_females_embark_third_port_purchase',
    'MEN6': 'num_men_disembark_second_landing',
    'WOMEN6': 'num_women_disembark_second_landing',
    'BOY6': 'num_boy_disembark_second_landing',
    'GIRL6': 'num_girl_disembark_second_landing',
    'ADULT6': 'num_adult_disembark_second_landing',
    'CHILD6': 'num_child_disembark_second_landing',
    'INFANT6': 'num_infant_disembark_second_landing',
    'MALE6': 'num_males_disembark_second_landing',
    'FEMALE6': 'num_females_disembark_second_landing'
}

impute_slave_number_var_map = {
    'SLAXIMP': 'imp_total_num_slaves_embarked',
    'SLAMIMP': 'imp_total_num_slaves_disembarked',
    'VYMRTIMP': 'imp_mortality_during_voyage',
    'ADLT1IMP': 'imp_num_adult_embarked',
    'CHIL1IMP': 'imp_num_children_embarked',
    'MALE1IMP': 'imp_num_male_embarked',
    'FEML1IMP': 'imp_num_female_embarked',
    'SLAVEMA1': 'total_slaves_embarked_age_identified',
    'SLAVEMX1': 'total_slaves_embarked_gender_identified',
    'ADLT2IMP': 'imp_adult_death_middle_passage',
    'CHIL2IMP': 'imp_child_death_middle_passage',
    'MALE2IMP': 'imp_male_death_middle_passage',
    'FEML2IMP': 'imp_female_death_middle_passage',
    'ADLT3IMP': 'imp_num_adult_landed',
    'CHIL3IMP': 'imp_num_child_landed',
    'MALE3IMP': 'imp_num_male_landed',
    'FEML3IMP': 'imp_num_female_landed',
    'SLAVEMA3': 'total_slaves_landed_age_identified',
    'SLAVEMX3': 'total_slaves_landed_gender_identified',
    'SLAVEMA7': 'total_slaves_dept_or_arr_age_identified',
    'SLAVEMX7': 'total_slaves_dept_or_arr_gender_identified',
    'TSLMTIMP': 'imp_slaves_embarked_for_mortality',
    'MEN7': 'imp_num_men_total',
    'WOMEN7': 'imp_num_women_total',
    'BOY7': 'imp_num_boy_total',
    'GIRL7': 'imp_num_girl_total',
    'ADULT7': 'imp_num_adult_total',
    'CHILD7': 'imp_num_child_total',
    'MALE7': 'imp_num_males_total',
    'FEMALE7': 'imp_num_females_total',
    'MENRAT7': 'percentage_men',
    'WOMRAT7': 'percentage_women',
    'BOYRAT7': 'percentage_boy',
    'GIRLRAT7': 'percentage_girl',
    'MALRAT7': 'percentage_male',
    'CHILRAT7': 'percentage_child',
    'VYMRTRAT': 'imp_mortality_ratio',
    'JAMCASPR': 'imp_jamaican_cash_price'
}

all_slave_number_var_map = slave_number_var_map.copy()
all_slave_number_var_map.update(impute_slave_number_var_map)


def voyage_to_dict(voyage):
    dikt = {}
    # Ship, nation, owners
    VoyageCache.load()
    ship = voyage.voyage_ship

    def get_label(obj, field='name'):
        if obj is None:
            return None
        return getattr(obj, field)

    if ship is not None:
        dikt['name_of_vessel'] = ship.ship_name
        dikt['year_ship_constructed'] = ship.year_of_construction
        dikt['year_ship_registered'] = ship.registered_year
        dikt['national_carrier'] = ship.nationality_ship_id
        dikt['national_carrier_name'] = VoyageCache.nations.get(
            ship.nationality_ship_id)
        dikt['ship_construction_place'] = ship.vessel_construction_place_id
        dikt['ship_construction_place_name'] = get_label(
            VoyageCache.ports.get(ship.vessel_construction_place_id))
        dikt['ship_registration_place'] = ship.registered_place_id
        dikt['ship_registration_place_name'] = get_label(
            VoyageCache.ports.get(ship.registered_place_id))
        dikt['rig_of_vessel'] = ship.rig_of_vessel_id
        dikt['rig_of_vessel_name'] = get_label(
            VoyageCache.rigs.get(ship.rig_of_vessel_id), 'label')
        dikt['tonnage_of_vessel'] = ship.tonnage
        dikt['ton_type'] = ship.ton_type_id
        dikt['ton_type_name'] = get_label(
            VoyageCache.ton_types.get(ship.ton_type_id), 'label')
        dikt['guns_mounted'] = ship.guns_mounted
        owners = list(
            VoyageShipOwnerConnection.objects.filter(voyage=voyage).extra(
                order_by=['owner_order']))
        if len(owners) > 0:
            dikt['first_ship_owner'] = owners[0].owner.name
        if len(owners) > 1:
            dikt['second_ship_owner'] = owners[1].owner.name
        if len(owners) > 2:
            dikt['additional_ship_owners'] = '\n'.join(
                [x.owner.name for x in owners[2:]])
    # Outcome
    outcome = voyage.voyage_name_outcome.get()
    if outcome is not None:
        dikt['voyage_outcome'] = outcome.particular_outcome_id
        dikt['african_resistance'] = outcome.resistance_id
        dikt['voyage_outcome_name'] = get_label(
            VoyageCache.particular_outcomes.get(outcome.particular_outcome_id),
            'label')
        dikt['african_resistance_name'] = get_label(
            VoyageCache.resistances.get(outcome.resistance_id), 'label')
    itin = voyage.voyage_itinerary
    if itin is not None:
        dikt[
            'first_port_intended_embarkation'] = itin.int_first_port_emb_id
        dikt[
            'second_port_intended_embarkation'] = itin.int_second_port_emb_id
        dikt[
            'first_port_intended_disembarkation'] = itin.int_first_port_dis_id
        dikt[
            'second_port_intended_disembarkation'
        ] = itin.int_second_port_dis_id
        dikt['port_of_departure'] = itin.port_of_departure_id
        dikt[
            'number_of_ports_called_prior_to_slave_purchase'
        ] = itin.ports_called_buying_slaves
        dikt[
            'first_place_of_slave_purchase'
        ] = itin.first_place_slave_purchase_id
        dikt[
            'second_place_of_slave_purchase'
        ] = itin.second_place_slave_purchase_id
        dikt[
            'third_place_of_slave_purchase'
        ] = itin.third_place_slave_purchase_id
        dikt[
            'principal_place_of_slave_purchase'
        ] = itin.principal_place_of_slave_purchase_id
        dikt[
            'place_of_call_before_atlantic_crossing'
        ] = itin.port_of_call_before_atl_crossing_id
        dikt[
            'number_of_new_world_ports_called_prior_to_disembarkation'
        ] = itin.number_of_ports_of_call
        dikt['first_place_of_landing'] = itin.first_landing_place_id
        dikt['second_place_of_landing'] = itin.second_landing_place_id
        dikt['third_place_of_landing'] = itin.third_landing_place_id
        dikt[
            'principal_place_of_slave_disembarkation'
        ] = itin.principal_port_of_slave_dis_id
        dikt['port_voyage_ended'] = itin.place_voyage_ended_id
        # Port names.
        dikt['first_port_intended_embarkation_name'] = get_label(
            VoyageCache.ports.get(itin.int_first_port_emb_id))
        dikt['second_port_intended_embarkation_name'] = get_label(
            VoyageCache.ports.get(itin.int_second_port_emb_id))
        dikt['first_port_intended_disembarkation_name'] = get_label(
            VoyageCache.ports.get(itin.int_first_port_dis_id))
        dikt['second_port_intended_disembarkation_name'] = get_label(
            VoyageCache.ports.get(itin.int_second_port_dis_id))
        dikt['port_of_departure_name'] = get_label(
            VoyageCache.ports.get(itin.port_of_departure_id))
        dikt['first_place_of_slave_purchase_name'] = get_label(
            VoyageCache.ports.get(itin.first_place_slave_purchase_id))
        dikt['second_place_of_slave_purchase_name'] = get_label(
            VoyageCache.ports.get(itin.second_place_slave_purchase_id))
        dikt['third_place_of_slave_purchase_name'] = get_label(
            VoyageCache.ports.get(itin.third_place_slave_purchase_id))
        dikt['principal_place_of_slave_purchase_name'] = get_label(
            VoyageCache.ports.get(
                itin.principal_place_of_slave_purchase_id))
        dikt['place_of_call_before_atlantic_crossing_name'] = get_label(
            VoyageCache.ports.get(
                itin.port_of_call_before_atl_crossing_id))
        dikt['first_place_of_landing_name'] = get_label(
            VoyageCache.ports.get(itin.first_landing_place_id))
        dikt['second_place_of_landing_name'] = get_label(
            VoyageCache.ports.get(itin.second_landing_place_id))
        dikt['third_place_of_landing_name'] = get_label(
            VoyageCache.ports.get(itin.third_landing_place_id))
        dikt['principal_place_of_slave_disembarkation_name'] = get_label(
            VoyageCache.ports.get(itin.principal_port_of_slave_dis_id))
        dikt['port_voyage_ended_name'] = get_label(
            VoyageCache.ports.get(itin.place_voyage_ended_id))
    dates = voyage.voyage_dates
    if dates is not None:
        dikt['date_departure'] = dates.voyage_began
        dikt['date_slave_purchase_began'] = dates.slave_purchase_began
        dikt['date_vessel_left_last_slaving_port'] = dates.vessel_left_port
        dikt['date_first_slave_disembarkation'] = dates.first_dis_of_slaves
        dikt[
            'date_second_slave_disembarkation'
        ] = dates.arrival_at_second_place_landing
        dikt['date_third_slave_disembarkation'] = dates.third_dis_of_slaves
        dikt['date_return_departure'] = dates.departure_last_place_of_landing
        dikt['date_voyage_completed'] = dates.voyage_completed
        dikt['length_of_middle_passage'] = dates.length_middle_passage_days
    numbers = voyage.voyage_slaves_numbers
    if numbers is not None:
        for k, v in list(slave_number_var_map.items()):
            dikt[number_prefix + k] = getattr(numbers, v)

    # Captains
    captains = voyage.voyage_captain.all()
    captain_keys = ['first', 'second', 'third']
    for i, captain in enumerate(captains):
        dikt[captain_keys[i] + '_captain'] = captain.name
    # Crew numbers
    crew = voyage.voyage_crew
    if crew is not None:
        dikt[number_prefix + 'CREW1'] = crew.crew_voyage_outset
        dikt[number_prefix + 'CREW2'] = crew.crew_departure_last_port
        dikt[number_prefix + 'CREW3'] = crew.crew_first_landing
        dikt[number_prefix + 'CREW4'] = crew.crew_return_begin
        dikt[number_prefix + 'CREW5'] = crew.crew_end_voyage
        dikt[number_prefix + 'CREW'] = crew.unspecified_crew
        dikt[
            number_prefix + 'SAILD1'] = crew.crew_died_before_first_trade
        dikt[
            number_prefix + 'SAILD2'] = crew.crew_died_while_ship_african
        dikt[number_prefix + 'SAILD3'] = crew.crew_died_middle_passage
        dikt[number_prefix + 'SAILD4'] = crew.crew_died_in_americas
        dikt[number_prefix + 'SAILD5'] = crew.crew_died_on_return_voyage
        dikt[number_prefix + 'CREWDIED'] = crew.crew_died_complete_voyage
        dikt[number_prefix + 'NDESERT'] = crew.crew_deserted
    return dikt


@login_required()
def editor_main(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    return render(request, 'contribute/editor_main.html')


def get_reviews_by_status(statuses, display_interim_data=False):
    filter_args = {'status__in': statuses}
    contributions = get_filtered_contributions(filter_args)

    def get_nation_label(nation):
        return nation.label if nation else ''

    def get_place_str(place):
        if place is None:
            return ''
        return place.region.region + '/' + place.place

    # Load all necessary voyage id data in a single query for better
    # efficiency.
    all_voyage_ids = {
        id for ids in
        [x['contribution'].get_related_voyage_ids() for x in contributions]
        for id in ids
    }
    fetched_voyages = Voyage.all_dataset_objects \
        .filter(voyage_id__in=all_voyage_ids) \
        .select_related('voyage_ship') \
        .select_related('voyage_ship__imputed_nationality') \
        .select_related('voyage_dates') \
        .select_related('voyage_slaves_numbers') \
        .select_related(
            'voyage_itinerary__imp_principal_place_of_slave_purchase') \
        .select_related(
            'voyage_itinerary__imp_principal_place_of_slave_purchase__region')\
        .select_related('voyage_itinerary__imp_principal_port_slave_dis') \
        .select_related(
            'voyage_itinerary__imp_principal_port_slave_dis__region')
    fetched_voyages_dict = {v.id: v for v in fetched_voyages}

    # Load all review requests that will be needed.
    review_requests_dict = {}
    review_requests_filtered = ReviewRequest.objects \
        .select_related('suggested_reviewer') \
        .filter(
            contribution_id__in=[full_contribution_id(
                info['type'], info['id']) for info in contributions],
            archived=False)
    for req in review_requests_filtered:
        if req.contribution_id in review_requests_dict:
            raise Exception(
                'Invalid state: more than one review request is active')
        review_requests_dict[req.contribution_id] = req

    # Load all interim voyages and editor contributions.
    editor_contributions = EditorVoyageContribution.objects.filter(
        request__id__in=[r.pk for r in list(review_requests_dict.values())])
    editor_contributions_req_dict = {}
    for e in editor_contributions:
        if e.request_id in editor_contributions_req_dict:
            continue
        editor_contributions_req_dict[e.request_id] = e

    contribs = [info['contribution'] for info in contributions]
    interim_ids = [
        c.interim_voyage_id
        for c in contribs
        if hasattr(c, 'interim_voyage_id')
    ] + [
        e.interim_voyage_id
        for e in list(editor_contributions_req_dict.values())
    ]
    interim_voyages_dict = {
        interim.pk:
        interim for interim in
         InterimVoyage.objects.
         select_related('imputed_national_carrier').
         select_related('imputed_principal_place_'
                        'of_slave_purchase__region').
         select_related('imputed_principal_port_'
                        'of_slave_disembarkation__region').
         filter(pk__in=interim_ids)
    }

    def get_contribution_info(info):
        contrib = info['contribution']
        voyage_ids = contrib.get_related_voyage_ids()
        # A voyage might have been deleted (and thus the contribution
        # points to a non-existent entry), so we make sure to
        # safely get them from the fetched dict.
        voyages = [v for v in [fetched_voyages_dict.get(id) for id in voyage_ids] if v is not None]
        voyage_ids = [v.voyage_id for v in voyages]
        voyage_ship = [v.voyage_ship.ship_name for v in voyages]
        voyage_years = [
            VoyageDates.get_date_year(
                v.voyage_dates.imp_arrival_at_port_of_dis)
            for v in voyages
        ]
        voyage_nation = [
            get_nation_label(
                v.voyage_ship.imputed_nationality) for v in voyages]
        voyage_exported = [
            v.voyage_slaves_numbers.imp_total_num_slaves_embarked
            for v in voyages
        ]
        voyage_imported = [
            v.voyage_slaves_numbers.imp_total_num_slaves_disembarked
            for v in voyages
        ]
        voyage_purchase_place = [
            get_place_str(
                v.voyage_itinerary.imp_principal_place_of_slave_purchase)
            for v in voyages
        ]
        voyage_landing_place = [
            get_place_str(v.voyage_itinerary.imp_principal_port_slave_dis)
            for v in voyages
        ]
        voyage_info = [
            str(v.voyage_ship.ship_name) + u' (' + str(
                VoyageDates.get_date_year(
                    v.voyage_dates.imp_arrival_at_port_of_dis)) + ')'
            for v in voyages
        ]
        # Fetch review info.
        active_request = review_requests_dict.get(
            full_contribution_id(info['type'], info['id']))
        if (active_request and
                active_request.created_voyage_id and
                active_request.requires_created_voyage_id()):
            voyage_ids = [active_request.created_voyage_id]
        if (display_interim_data and not isinstance(
                contrib, DeleteVoyageContribution)) or isinstance(
                    contrib, NewVoyageContribution):
            # Must fill elements above with interim data.
            interim = interim_voyages_dict.get(contrib.interim_voyage_id)
            if active_request:
                editor_contrib = editor_contributions_req_dict.get(
                    active_request.id)
                if editor_contrib:
                    interim = interim_voyages_dict.get(
                        editor_contrib.interim_voyage_id)
            voyage_ship = [interim.name_of_vessel]
            voyage_years = [interim.imputed_year_voyage_began]
            voyage_nation = [get_nation_label(
                interim.imputed_national_carrier)]
            voyage_exported = [interim.imputed_total_slaves_embarked]
            voyage_imported = [interim.imputed_total_slaves_disembarked]
            voyage_purchase_place = [
                get_place_str(
                    interim.imputed_principal_place_of_slave_purchase)
            ]
            voyage_landing_place = [
                get_place_str(
                    interim.imputed_principal_port_of_slave_disembarkation)
            ]
            voyage_info = [interim.name_of_vessel]
        res = {
            'type': info['type'],
            'id': info['id'],
            'contributor': contrib.contributor.get_full_name(),
            'date_created': contrib.date_created,
            'voyage_ids': voyage_ids,
            'voyage_info': voyage_info,
            'voyage_ship': voyage_ship,
            'voyage_years': voyage_years,
            'voyage_nation': voyage_nation,
            'voyage_exported': voyage_exported,
            'voyage_imported': voyage_imported,
            'voyage_purchase_place': voyage_purchase_place,
            'voyage_landing_place': voyage_landing_place
        }
        if active_request:
            res['review_request_id'] = active_request.pk
            res['reviewer'] = active_request.suggested_reviewer.get_full_name()
            res['response_id'] = active_request.response
            res['response'] = (
                active_request.get_status_msg()
                if active_request.final_decision in [
                    ReviewRequestDecision.under_review,
                    ReviewRequestDecision.begun_editorial_review
                ] else u_('Posted'))
            res['reviewer_comments'] = active_request.reviewer_comments
            res['reviewer_final_decision'] = active_request.get_status_msg()
            if active_request.final_decision:
                # Fetch if of the editor's contribution.
                res['editor_contribution_id'] = editor_contributions_req_dict[
                    active_request.pk].pk
        else:
            res['review_request_id'] = 0
            res['reviewer'] = ''
            res['response_id'] = 0
            res['response'] = ''
            res['reviewer_comments'] = ''
            res['status'] = 'No reviewer assigned'
            res['reviewer_final_decision'] = ''
            res['editor_contribution_id'] = 0
        return res

    return {
        full_contribution_id(x['type'], x['id']): get_contribution_info(x)
        for x in contributions
    }


@login_required()
@never_cache
def get_pending_requests(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    return JsonResponse(
        get_reviews_by_status(ContributionStatus.active_statuses, False))


@login_required()
def get_reviewers(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    reviewers = [{
        'full_name': u.get_full_name(),
        'pk': u.pk
    } for u in User.objects.filter(is_staff=True)]
    return JsonResponse(reviewers, safe=False)


@login_required()
def get_pending_publication(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    return JsonResponse(
        get_reviews_by_status([ContributionStatus.approved], True))


def assert_limit_active_review_requests(contrib_id, max_allowed=0):
    reqs = [
        req
        for req in ReviewRequest.objects.filter(contribution_id=contrib_id)
        if not req.archived
    ]
    if len(reqs) > max_allowed:
        return JsonResponse({
            'error':
            u_('There is already an active review for this contribution')
        })
    return None


def override_empty_fields_with_single_value(interim_voyage, review_request):
    # Fetch pre-existing data, if the interim value is
    # not set and there is a single non-null value at one of
    # the previous interim/voyage data records, we override
    # the null value with that single value.
    def get_dict_from_interim(interim):
        data = {
            k: v
            for k, v in list(interim.__dict__.items())
            if not k.startswith('_') and v
        }
        # Now we must load numbers
        numbers = {
            number_prefix + n.var_name: n.number
            for n in interim.slave_numbers.all()
        }
        data.update(numbers)
        return data

    user_contribution = review_request.contribution()
    if user_contribution is None:
        raise Http404
    existing_data = contribution_related_data(user_contribution)
    existing_data['user'] = get_dict_from_interim(
        user_contribution.interim_voyage)
    # Fetch user and reviewer contributions (if any) and map to dict (use
    # __dict__ ?).
    review_contribution = review_request.review_contribution.first()
    if review_contribution:
        existing_data['reviewer'] = get_dict_from_interim(
            review_contribution.interim_voyage)
    # First pass, build a dictionary indexed by field with
    # the first non-null value found for that field, if the key is
    # already in the dictionary, we check to see if the value is
    # the same, if they differ, we update the field to None so that
    # no value gets propagated.
    foreign_keys = {
        f.name: f.name + '_id'
        for f in InterimVoyage._meta.get_fields()
        if isinstance(f, Field) and f.get_internal_type() == 'ForeignKey'
    }
    single_values = {}
    for data in existing_data.values():
        for k, v in data.items():
            if v is None or v == '': continue
            if k.startswith('date') and v == ',,': continue
            k = foreign_keys.get(k, k)
            if k in single_values and single_values[k] != v:
                single_values[k] = None
            else:
                single_values[k] = v
    # Second pass, set values of interim_voyage.
    numbers = []
    for k, v in list(single_values.items()):
        if not v:
            continue
        if k.startswith(number_prefix):
            num = InterimSlaveNumber()
            num.var_name = k[len(number_prefix):]
            num.number = v
            numbers.append(num)
        elif hasattr(interim_voyage, k):
            setattr(interim_voyage, k, v)
    with transaction.atomic():
        interim_voyage.save(force_update=True)
        for num in numbers:
            num.interim_voyage = interim_voyage
            num.save()
    return interim_voyage


@login_required()
@require_POST
def begin_editorial_review(request):
    """
    The editor can start an editorial review without going
    through a reviewer. In this case we will produce a 'dummy'
    review request and immediately clone the editorial form.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    contribution_id = request.POST.get('contribution_id')
    contribution = get_contribution_from_id(contribution_id)
    if contribution is None:
        raise Http404
    with transaction.atomic():
        set_isolation_serializable()
        assertion = assert_limit_active_review_requests(contribution_id, 0)
        if assertion:
            return assertion
        reviewer = request.user
        review_request = ReviewRequest()
        review_request.editor = request.user
        review_request.editor_comments = (
            'Editorial review bypassing a reviewer')
        review_request.email_sent = False
        review_request.contribution_id = contribution_id
        review_request.suggested_reviewer = reviewer
        review_request.response = ReviewRequestResponse.begun_editorial_review
        review_request.final_decision = \
            ReviewRequestDecision.begun_editorial_review
        review_request.save()
        contribution.status = ContributionStatus.under_review
        contribution.save()
        contributor_prefix = 'Contributor: '
        for e in review_request.editor_contribution.all():
            e.delete()
        editor_contribution = EditorVoyageContribution()
        editor_contribution.request = review_request
        editor_contribution.notes = contributor_prefix + \
            contribution.notes if contribution.notes else ''
        has_interim_voyage = hasattr(contribution, 'interim_voyage')
        editor_contribution.ran_impute = not has_interim_voyage
        if has_interim_voyage:
            editor_contribution.interim_voyage = clone_interim_voyage(
                contribution, contributor_prefix)
            override_empty_fields_with_single_value(
                editor_contribution.interim_voyage, review_request)
        editor_contribution.save()
        editor_contribution_id = editor_contribution.pk
    return JsonResponse({
        'review_request_id': review_request.pk,
        'editor_contribution_id': editor_contribution_id
    })


@login_required()
@require_POST
def post_review_request(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    contribution_id = request.POST.get('contribution_id')
    contribution = get_contribution_from_id(contribution_id)
    if contribution is None:
        raise Http404
    reviewer_id = int(request.POST.get('reviewer_id'))
    message = request.POST.get('message')
    if contribution.contributor_id == reviewer_id:
        return JsonResponse({
            'error': u_('Reviewer and contributor must be different users')
        })

    review_request = ReviewRequest()
    try:
        with transaction.atomic():
            set_isolation_serializable()
            if request.POST.get('archive_active_requests'):
                ReviewRequest.objects.filter(
                    contribution_id=contribution_id,
                    archived=False).update(archived=True)
            else:
                assertion = assert_limit_active_review_requests(
                    contribution_id, 0)
                if assertion:
                    return assertion
            reviewer = get_object_or_404(User, pk=reviewer_id)
            review_request.editor = request.user
            review_request.editor_comments = message
            review_request.email_sent = False
            review_request.contribution_id = contribution_id
            review_request.suggested_reviewer = reviewer
            review_request.save()
            contribution.status = ContributionStatus.under_review
            contribution.save()
    except Exception as e:
        return JsonResponse({'error': str(e)})

    result = 0
    try:
        reply_url = settings.WEBSITE_ROOT + \
            '/contribute/reply_review_request/' + str(review_request.pk)
        result = send_mail('Voyages - contribution review request',
                           'Editor message:\r\n' + message + '\n\n'
                           'Please visit ' + reply_url + '\r\nto reply.',
                           settings.CONTRIBUTE_SENDER_EMAIL, [reviewer.email],
                           html_message='<strong>Editor message:'
                           '</strong><p>' + message + '</p>'
                           '<p>Please click '
                           '<a href="' + reply_url + '">here</a>'
                           ' to reply.</p>')
    except Exception:
        traceback.print_exc()
    finally:
        if result == 1:
            review_request.email_sent = True
            review_request.save()

    return JsonResponse({'review_request': review_request.pk})


@login_required()
@require_POST
def post_archive_review_request(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    contribution_id = request.POST.get('contribution_id')
    reqs = [
        req
        for req
        in ReviewRequest.objects.filter(contribution_id=contribution_id)
        if not req.archived
    ]
    if len(reqs) == 0:
        return JsonResponse({
            'error': u_('There is no active review for this contribution')
        })
    for req in reqs:
        with transaction.atomic():
            contribution = req.contribution()
            contribution.status = ReviewRequestDecision.under_review
            contribution.save()
            req.archived = True
            req.save()
    return JsonResponse({'result': len(reqs)})


@login_required()
def review_request(request, review_request_id):
    req = get_object_or_404(ReviewRequest, pk=review_request_id)
    if req.archived or req.suggested_reviewer_id != request.user.pk:
        return HttpResponseForbidden()
    if req.review_contribution.first():
        return HttpResponseRedirect(
            reverse('contribute:review',
                    kwargs={'review_request_id': review_request_id}))
    contribution = req.contribution()
    if contribution is None:
        raise Http404
    return render(request, 'contribute/review_request.html', {
        'request': req,
        'contribution': contribution
    })


def clone_interim_voyage(contribution, contributor_comment_prefix):
    """
    Clone an interim voyage and all of its child models.
    This is used to obtain an editable reviewer or editor version of
    the user contribution.
    Should be executed within a transaction to ensure that all
    db changes are valid.
    """
    interim = contribution.interim_voyage
    if interim is None:
        return None
    related_models = list(chain(
        interim.article_sources.all(),
        interim.book_sources.all(),
        interim.newspaper_sources.all(),
        interim.private_note_or_collection_sources.all(),
        interim.unpublished_secondary_sources.all(),
        interim.primary_sources.all(),
        interim.pre_existing_sources.all(),
        interim.slave_numbers.all()))
    interim.pk = None
    # Prepend comments with contributor name.
    changed = {}
    try:
        note_dict = json.loads(interim.notes) if interim.notes else {}
    except Exception:
        note_dict = {'parse_error': interim.notes}
    for key, note in list(note_dict.items()):
        changed[key] = escape(contributor_comment_prefix + note)

    with transaction.atomic():
        interim.notes = json.dumps(changed)
        interim.save()
        for item in related_models:
            item.pk = None
            item.interim_voyage = interim
            if (hasattr(item, 'notes') and
                    item.notes is not None and
                    item.notes != ''):
                item.notes = escape(contributor_comment_prefix + item.notes)
            item.save()
        return interim


@login_required()
@require_POST
def reply_review_request(request):
    review_request_id = request.POST.get('review_request_id')
    req = get_object_or_404(ReviewRequest, pk=review_request_id)

    if req.suggested_reviewer_id != request.user.pk:
        return HttpResponseForbidden()

    redirect = HttpResponseRedirect(
        reverse('contribute:review',
                kwargs={'review_request_id': review_request_id}))
    if req.review_contribution.count() > 0:
        return redirect

    # Check response
    response = request.POST.get('response')
    valid_responses = ['accept', 'reject']
    if response not in valid_responses:
        return HttpResponseBadRequest()
    req.response = (ReviewRequestResponse.accepted
                    if response == 'accept'
                    else ReviewRequestResponse.rejected)
    req.reviewer_comments = request.POST.get('message_to_editor')
    with transaction.atomic():
        req.save()
        if response == 'accept':
            review = ReviewVoyageContribution()
            review.request = req
            contribution = req.contribution()
            if contribution is None:
                raise Http404
            if hasattr(contribution, 'interim_voyage'):
                review.interim_voyage = clone_interim_voyage(
                    contribution, 'Contributor: ')
            review.notes = ('Contributor: ' + contribution.notes
                            if contribution.notes else '')
            review.save()
        else:
            redirect = HttpResponseRedirect(reverse('contribute:index'))
    return redirect


def interim_data(interim):
    dikt = {
        number_prefix + n.var_name: n.number
        for n in interim.slave_numbers.all()
        if n.number is not None
    }
    fields = [
        f for f in InterimVoyage._meta.get_fields() if isinstance(f, Field)
    ]
    for field in fields:
        # Check if this is a foreign key.
        name = field.name
        value = getattr(interim, field.name)
        if value is None:
            continue
        internal_type = field.get_internal_type()
        if internal_type == 'ForeignKey':
            try:
                dikt[name] = value.pk
                dikt[name + '_name'] = str(value)
            except Exception:
                pass
        elif internal_type in [
                'IntegerField', 'CharField', 'TextField',
                'CommaSeparatedIntegerField'
        ]:
            if value != '':
                dikt[name] = value
    return dikt


@login_required()
def review(request, review_request_id):
    req = get_object_or_404(ReviewRequest, pk=review_request_id)
    if any([req.archived,
            req.response == 2,
            req.final_decision != 0,
            req.suggested_reviewer_id != request.user.pk]):
        return HttpResponseForbidden()
    if req.response == 0:
        return HttpResponseRedirect(
            reverse('contribute:review_request',
                    kwargs={'review_request_id': review_request_id}))
    contribution_id = req.contribution_id
    user_contribution = req.contribution()
    if user_contribution is None:
        raise Http404
    if contribution_id.startswith('delete'):
        return delete_review_render(request, user_contribution, True,
                                    'reviewer')
    review_contribution = req.review_contribution.first()
    interim = (review_contribution.interim_voyage
               if review_contribution else None)
    if interim is None:
        raise Exception('Could not find reviewer\'s interim form')
    (_, form, numbers, _) = interim_main(request,
                                         review_contribution,
                                         interim)
    sources_post = None if request.method != 'POST' else request.POST.get(
        'sources')
    # Build previous data dictionary.
    # For the review we need to include both the original voyage(s) data
    # as well as the user contribution itself.
    previous_data = contribution_related_data(user_contribution)
    previous_data[u_('User contribution')] = interim_data(
        user_contribution.interim_voyage)
    return render(
        request, 'contribute/interim.html', {
            'form': form,
            'mode': 'review',
            'contribution': review_contribution,
            'numbers': numbers,
            'interim': interim,
            'sources_post': sources_post,
            'voyages_data': json.dumps(previous_data)
        })


@login_required()
def editorial_review(request, review_request_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    review_request = get_object_or_404(ReviewRequest, pk=review_request_id)
    contribution = review_request.editor_contribution.first()
    contribution_id = review_request.contribution_id
    user_contribution = review_request.contribution()
    if user_contribution is None:
        raise Http404
    if contribution_id.startswith('delete'):
        return delete_review_render(request, user_contribution, True, 'editor')
    review_contribution = review_request.review_contribution.first()
    reviewer_interim = (review_contribution.interim_voyage
                        if review_contribution else None)
    sources_post = None if request.method != 'POST' else request.POST.get(
        'sources')
    # Build previous data dictionary.
    # Include pre-existing voyage data, user contribution, and reviewer
    # version.
    previous_data = contribution_related_data(user_contribution)
    previous_data[u_('User contribution')] = interim_data(
        user_contribution.interim_voyage)
    if reviewer_interim:
        previous_data[u_('Reviewer')] = interim_data(reviewer_interim)
    editor_interim = contribution.interim_voyage
    (_, form, numbers, _) = interim_main(request, contribution, editor_interim)
    return render(
        request, 'contribute/interim.html', {
            'form': form,
            'mode': 'editorial_review',
            'contribution': contribution,
            'numbers': numbers,
            'interim': editor_interim,
            'sources_post': sources_post,
            'voyages_data': json.dumps(previous_data)
        })


@login_required()
@require_POST
def submit_editorial_decision(request, editor_contribution_id):
    contribution = get_object_or_404(EditorVoyageContribution,
                                     pk=editor_contribution_id)
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    decision = -1
    created_voyage_id = None
    try:
        decision = int(request.POST['editorial_decision'])
        voyage_id = request.POST.get('created_voyage_id')
        if voyage_id:
            created_voyage_id = int(voyage_id)
    except Exception:
        pass
    if decision not in [
            ReviewRequestDecision.accepted_by_editor,
            ReviewRequestDecision.rejected_by_editor,
            ReviewRequestDecision.deleted
    ]:
        return HttpResponseBadRequest()
    if all([decision == ReviewRequestDecision.accepted_by_editor,
            contribution.interim_voyage,
            not contribution.ran_impute]):
        return JsonResponse({
            'result': 'Failed',
            'errors': u_('Impute program must be ran on contribution before '
                         'acceptance')
        })
    if all([decision == ReviewRequestDecision.accepted_by_editor,
            contribution.interim_voyage]):
        # Check whether every new source in the editorial version has been
        # created in the system before continuing.
        all_sources = get_all_new_sources_for_interim(
            contribution.interim_voyage.pk)
        for src in all_sources:
            created_src = src.created_voyage_sources
            if not created_src:
                return JsonResponse({
                    'result': 'Failed',
                    'errors': u_('All new sources must be created before this '
                                 'submission is accepted.')
                })
            if not src.source_ref_text or not src.source_ref_text.startswith(
                    created_src.short_ref):
                return JsonResponse({
                    'result': 'Failed',
                    'errors': u_('New sources must have a connection '
                                 'reference starting with the source\'s short '
                                 'reference.')
                })

    # If the editor accepts a new/merge contribution, a voyage id for the
    # published voyage must be specified.
    review_request = contribution.request
    user_contribution = review_request.contribution()
    if user_contribution is None:
        raise Http404
    if not created_voyage_id:
        if review_request.requires_created_voyage_id(
        ) and decision == ReviewRequestDecision.accepted_by_editor:
            return JsonResponse({
                'result': 'Failed',
                'errors': u_('Expected a voyage id for new/merge contribution')
            })
    else:
        # We must check whether this is a unique id (with respect to
        # pre-existing and next publication batch).
        if (Voyage.all_dataset_objects.filter(
                voyage_id=created_voyage_id).count() > 0 and
                created_voyage_id and
                created_voyage_id not in
                user_contribution.get_related_voyage_ids()):
            # Only case when this is allowed is if a merge contribution
            # uses one of the merged voyages ids.
            return JsonResponse({
                'result': 'Failed',
                'errors': u_('Voyage id already exists')
            })
        if ReviewRequest.objects.filter(
                created_voyage_id=created_voyage_id,
                archived=False).exclude(pk=review_request.pk).count() > 0:
            return JsonResponse({
                'result': 'Failed',
                'errors': u_('Voyage id already in current publication batch')
            })

    with transaction.atomic():
        # Save interim form.
        if contribution.interim_voyage:
            (valid, form, *_) = interim_main(request, contribution,
                                             contribution.interim_voyage)
            if not valid:
                return JsonResponse({'valid': valid, 'errors': form.errors})
            if decision == ReviewRequestDecision.accepted_by_editor:
                # Check if yearam and fate2 variables are set.
                missing_fields = []
                if not contribution.interim_voyage.imputed_year_arrived_at_port_of_disembarkation:
                    missing_fields.append('YEARAM')
                if not contribution.interim_voyage.imputed_outcome_of_voyage_for_slaves:
                    missing_fields.append('FATE2')
                if len(missing_fields) > 0:
                    transaction.set_rollback(True)
                    return JsonResponse({
                        'result': 'Failed',
                        'errors': ('Imputed field(s) %s is(are) mandatory' %
                                   ', '.join(missing_fields))
                    })

        # Fetch decision.
        review_request.final_decision = decision
        review_request.created_voyage_id = created_voyage_id
        is_iam = request.POST.get('is_intra_american', None) is not None
        review_request.dataset = (VoyageDataset.IntraAmerican if is_iam
                                  else VoyageDataset.Transatlantic)
        msg = request.POST.get('decision_message')
        msg = 'Editor: ' + msg if msg else ''
        msg = escape(msg)
        user_contribution.status = decision
        user_contribution.save()
        if decision == ReviewRequestDecision.deleted:
            review_request.archived = True
        review_request.decision_message = msg
        review_request.save()
    return JsonResponse({'result': 'OK'})


@login_required()
@require_POST
def submit_review_to_editor(request, review_request_id):
    req = get_object_or_404(ReviewRequest, pk=review_request_id)
    if req.archived or req.response != 1 or \
            req.suggested_reviewer_id != request.user.pk:
        return HttpResponseForbidden()
    decision = -1
    try:
        decision = int(request.POST['reviewer_decision'])
    except Exception:
        pass
    if decision not in (ReviewRequestDecision.accepted_by_reviewer,
                        ReviewRequestDecision.rejected_by_reviewer):
        return HttpResponseBadRequest()
    try:
        with transaction.atomic():
            # Save interim form.
            contribution = req.review_contribution.first()
            has_interim_voyage = hasattr(
                contribution, 'interim_voyage') and contribution.interim_voyage
            if has_interim_voyage:
                (valid, form, _, _) = interim_main(
                    request, contribution, contribution.interim_voyage)
                if not valid:
                    return JsonResponse({
                        'result': 'Failed',
                        'errors': form.errors
                    })
            # Save review request with decision.
            msg = request.POST.get('message_to_editor')
            msg = 'Reviewer: ' + msg if msg else ''
            msg = escape(msg)
            req.decision_message = msg
            req.final_decision = decision
            req.save()
            # Create an editor contribution with cloned review data.
            for e in req.editor_contribution.all():
                e.delete()
            editor_contribution = EditorVoyageContribution()
            editor_contribution.request = req
            editor_contribution.notes = escape(
                'Reviewer: ' + contribution.notes
                if contribution.notes else '')
            editor_contribution.ran_impute = not has_interim_voyage
            if has_interim_voyage:
                editor_contribution.interim_voyage = clone_interim_voyage(
                    contribution, 'Reviewer: ')
                override_empty_fields_with_single_value(
                    editor_contribution.interim_voyage, req)
            editor_contribution.save()
        return JsonResponse({'result': 'OK'})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'result': 'Failed', 'errors': [str(e)]})


@login_required()
@require_POST
def impute_contribution(request, editor_contribution_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    # First we save the current version of the interim voyage.
    contribution = get_object_or_404(EditorVoyageContribution,
                                     pk=editor_contribution_id)
    (valid, form, *_) = interim_main(request, contribution,
                                     contribution.interim_voyage)
    if not valid:
        return JsonResponse({'result': 'Failed', 'errors': form.errors})
    interim_voyage_id = contribution.interim_voyage_id
    # Reload the interim voyage from database, just in case.
    interim = get_object_or_404(InterimVoyage, pk=interim_voyage_id)
    is_iam = request.POST.get('is_intra_american', None) is not None
    impute_tuple = imputed.compute_imputed_vars(interim, is_iam)
    result = impute_tuple[0]
    imputed_numbers = impute_tuple[1]
    try:
        with transaction.atomic():
            contribution.ran_impute = True
            contribution.save()
            # Delete old numeric values.
            InterimSlaveNumber.objects.filter(interim_voyage__id=interim.pk,
                                            var_name__in=list(
                                                imputed_numbers.keys())).delete()
            # Map imputed fields back to the contribution, save it and yield
            # response.
            for k, v in list(result.items()):
                setattr(interim, k, v)
            interim.save()
            for k, v in list(imputed_numbers.items()):
                if not v:
                    continue
                number = InterimSlaveNumber()
                number.interim_voyage = interim
                number.var_name = k.upper()
                number.number = v
                number.save()
        return JsonResponse({
            'result': 'OK',
            'is_iam': is_iam,
            'imputed_vars': impute_tuple[2],
            'imputed_numbers': imputed_numbers
        })
    except:
        return JsonResponse({
            'result': 'FAILED',
            'is_iam': is_iam,
            'imputed_vars': impute_tuple[2],
            'imputed_numbers': imputed_numbers
        })


@login_required()
@require_POST
def editorial_sources(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    mode = request.POST.get('mode')
    if mode not in ['new', 'edit', 'save']:
        return HttpResponseBadRequest()
    original_ref = request.POST.get('original_ref')
    conn = VoyageSourcesConnection.objects.filter(
        text_ref=original_ref).first() if original_ref else None
    source = conn.source if conn else None
    if not source and request.POST.get('short_ref'):
        source = VoyageSources.objects.filter(
            short_ref=request.POST.get('short_ref')).first()
    if not source:
        source = VoyageSources()
    prefix = 'interim_source['
    plen = len(prefix)
    interim_source_dict = {
        k[plen:-1]: v
        for k, v in list(request.POST.items())
        if k.startswith(prefix) and v is not None
    }
    created_source_pk = interim_source_dict.get('created_voyage_sources_id')
    if conn is None and created_source_pk:
        source = VoyageSources.objects.get(pk=created_source_pk)
    if mode == 'save':
        form = VoyagesSourcesAdminForm(request.POST, instance=source)
        if not form.is_valid():
            return JsonResponse({'result': 'Failed', 'errors': form.errors})
        with transaction.atomic():
            # Save text reference in interim source.
            interim_source_id = request.POST.get('interim_source_id')
            connection_ref = request.POST.get('connection_ref', original_ref)
            if interim_source_id and (
                    not connection_ref or connection_ref == ''):
                return JsonResponse({
                    'result': 'Failed',
                    'errors': ['Text reference is mandatory']
                })
            reference = form.save()
            if interim_source_id and not connection_ref.startswith(
                    reference.short_ref):
                return JsonResponse({
                    'result': 'Failed',
                    'errors': ['Text reference must begin with '
                               'Source\'s short reference']
                })
            if interim_source_id:
                pair = interim_source_id.split('/')
                src_model = interim_source_model(pair[0])
                interim_source = None
                try:
                    interim_source = src_model.objects.get(pk=int(pair[1]))
                except Exception:
                    interim_source = src_model()
                    interim_source.interim_voyage = InterimVoyage(
                        pk=int(request.POST['interim_pk']))
                interim_source.source_ref_text = connection_ref
                interim_source.created_voyage_sources = reference
                interim_source.save()
                # Update the composite id in case we needed to create a new
                # entry.
                interim_source_id = pair[0] + '/' + str(interim_source.pk)
            return JsonResponse({
                'result': 'OK',
                'created_voyage_sources_id': reference.pk,
                'interim_source_id': interim_source_id
            })
    if mode == 'new':
        src_type = interim_source_dict['type']
        formatted_content = ''
        all_types = {
            x.group_name: x for x in VoyageSourcesType.objects.all()
        }
        if src_type == 'Primary source':
            formatted_content = '<em>' + \
                interim_source_dict['name_of_library_or_archive'] + \
                '</em> (' + \
                interim_source_dict['location_of_library_or_archive'] + ')'
            source.source_type = all_types['Documentary source']
        elif src_type == 'Article source':
            formatted_content = interim_source_dict['authors'] + \
                ' "' + interim_source_dict['article_title'] + '", <em>' + \
                interim_source_dict['journal'] + '</em>, ' + \
                interim_source_dict.get('volume_number', 'vol??') + \
                ' (' + interim_source_dict.get('year', 'year??') + '): ' + \
                interim_source_dict.get('page_start', 'page_start') + '-' + \
                interim_source_dict.get('page_end', 'page_end')
            source.source_type = all_types['Published source']
        elif src_type == 'Book source':
            formatted_content = interim_source_dict['authors'] + ','
            if interim_source_dict['source_is_essay_in_book'] == 'true':
                formatted_content += (
                    ' "' + interim_source_dict['essay_title'] + '",'
                    ' ' + interim_source_dict['editors'] + ' (ed.)')
            place = interim_source_dict.get('place_of_publication', 'place??')
            year = interim_source_dict.get('year', 'year??')
            formatted_content += (
                ' <em>' + interim_source_dict['book_title'] + '</em> '
                '(' + place + ', ' + year + ')')
            source.source_type = all_types['Published source']
        elif src_type == 'Newspaper source':
            alt_name = interim_source_dict.get('alternative_name')
            formatted_content = \
                '<em>' + interim_source_dict['name'] + '</em>' + \
                ((' (later, ' + alt_name + ')') if alt_name else '') + \
                ', (' + interim_source_dict.get('city', 'city??') + ', ' + \
                interim_source_dict.get('country', 'country??') + ')'
            source.source_type = all_types['Newspaper']
        elif src_type == 'Private note or collection source':
            formatted_content = interim_source_dict['authors'] + ', ' + \
                interim_source_dict['title'] + \
                ' (' + interim_source_dict.get('location', 'location??') + ')'
            source.source_type = all_types['Private note or collection']
        elif src_type == 'Unpublished secondary source':
            formatted_content = interim_source_dict['authors'] + ', ' + \
                interim_source_dict['title'] + \
                ' (' + interim_source_dict.get('location', 'location??') + ')'
            source.source_type = all_types['Unpublished secondary source']
        source.full_ref = formatted_content
    form = VoyagesSourcesAdminForm(instance=source)
    return render(request, 'contribute/sources_form.html', {
        'form': form,
        'original_ref': original_ref
    })


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


@login_required()
@require_POST
def download_voyages(request):
    statuses = []
    if request.POST.get('accepted_unpublished_check') == 'True':
        statuses.append(ContributionStatus.approved)
    if request.POST.get('under_review_check') == 'True':
        statuses.append(ContributionStatus.under_review)
    if request.POST.get('committed_check') == 'True':
        statuses.append(ContributionStatus.committed)
    if request.POST.get('rejected_check') == 'True':
        statuses.append(ContributionStatus.rejected)

    include_published = request.POST.get('published_check') == 'True'
    remove_linebreaks = request.POST.get('remove_linebreaks') == 'True'
    intra_american_flag = request.POST.get('intra_american_flag')
    if intra_american_flag:
        intra_american_flag = int(intra_american_flag)

    try:
        dloads = settings.MEDIA_ROOT + '/csv_downloads/'
        if not os.path.exists(dloads):
            os.makedirs(dloads)
        csv_file = tempfile.NamedTemporaryFile(
            dir=dloads, mode='w', delete=False)
        log_file = tempfile.NamedTemporaryFile(
            dir=dloads, mode='w', delete=False)
        _thread.start_new_thread(
            generate_voyage_csv_file,
            (statuses, include_published, csv_file, log_file,
             remove_linebreaks, intra_american_flag))
        return JsonResponse({
            'result': 'OK',
            'log_file': re.sub('^.*/', '', log_file.name),
            'csv_file': re.sub('^.*/', '', csv_file.name)
        })
    except Exception as exception:
        return JsonResponse({'result': 'Failed', 'error': repr(exception)})


def generate_voyage_csv_file(statuses,
                             published,
                             csv_file,
                             log_file,
                             remove_linebreaks=False,
                             intra_american_flag=None):

    def log(message):
        log_file.seek(0)
        log_file.truncate(0)
        log_file.write(message)
        log_file.flush()

    log('Started generating CSV file with statuses'
        '=' + str(statuses) + ', '
        'published=' + str(published) + ', '
        'intra_american_flag=' + str(intra_american_flag))
    count = 0
    try:
        # Simply iterate over generated CSV rows passing the file as buffer.
        for _ in get_voyages_csv_rows(statuses, published, csv_file,
                                      remove_linebreaks, intra_american_flag):
            count += 1
            if (count % 100) == 0:
                log(str(count) + ' rows exported to CSV')
        log('FINISHED')
    except Exception:
        error_message = 'ERROR occurred after ' + \
            str(count) + ' rows processed: ' + traceback.format_exc()
        print(error_message)
        log(error_message)
    csv_file.flush()
    csv_file.close()
    log_file.close()
    gc.collect()


@login_required()
@require_POST
def download_voyages_status(request):
    log_file = request.POST.get('log_file')
    if log_file is None:
        return JsonResponse({'result': 'Failed'})
    dloads = settings.MEDIA_ROOT + '/csv_downloads/'
    log_file = dloads + log_file
    status = 'Not started'
    with open(log_file, 'r') as f:
        status = f.readline()
    return JsonResponse({'result': 'OK', 'status': status})


def download_voyages_go(request):
    csv_file = request.GET.get('csv_file')
    if csv_file is None:
        raise Http404
    file_path = settings.MEDIA_ROOT + '/csv_downloads/' + csv_file
    data = None
    with open(file_path, "r") as f:
        data = f.read()
    response = HttpResponse(data, content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename=voyages.csv'
    return response


def get_voyages_csv_rows(statuses,
                         published,
                         buffer=None,
                         remove_linebreaks=False,
                         intra_american_flag=None):
    if buffer is None:
        buffer = Echo()
    writer = get_csv_writer(buffer)
    header = get_header_csv_text()
    yield header
    buffer.write(header)

    def row_processor(x):
        return x if not remove_linebreaks else \
            {k: re.sub('\r?\n', ' ', v) if isinstance(
                v, six.string_types) else v for k, v in list(x.items())}

    for item in export_contributions(statuses):
        yield safe_writerow(writer, row_processor(item))
    if published:
        for item in export_from_voyages(intra_american_flag):
            yield safe_writerow(writer, row_processor(item))


@login_required()
@require_POST
def publish_pending(request):
    # Here we are using a lightweight approach at background processing by
    # starting a thread and logging the progress to a file whose name is
    # returned in the response.
    try:
        pub_logs = settings.MEDIA_ROOT + '/publication_logs/'
        if not os.path.exists(pub_logs):
            os.makedirs(pub_logs)
        log_file = tempfile.NamedTemporaryFile(
            dir=pub_logs, mode='w', delete=False)
        _thread.start_new_thread(
            publish_accepted_contributions,
            (log_file, request.POST.get('skip_backup', False)))
        return JsonResponse({
            'result': 'OK',
            'log_file': re.sub('^.*/', '', log_file.name)
        })
    except Exception as exception:
        return JsonResponse({'result': 'Failed', 'error': repr(exception)})


@login_required()
@require_POST
def retrieve_publication_status(request):
    pub_logs = settings.MEDIA_ROOT + '/publication_logs/'
    log_file = pub_logs + request.POST['log_file']
    with open(log_file, 'r') as f:
        lines = f.readlines()
        skip_count = int(request.POST.get('skip_count', 0))
        text = ''
        i = skip_count
        while i < len(lines):
            text += lines[i] + '<br />'
            i += 1
        return JsonResponse({'lines': text, 'count': i - skip_count})
