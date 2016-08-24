# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.http import Http404
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from voyages.apps.contribute.forms import *
from voyages.apps.contribute.models import *
from voyages.apps.voyage.cache import VoyageCache
from voyages.apps.voyage.models import *
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.conf import settings
import imputed
import json

number_prefix = 'interim_slave_number_'

def full_contribution_id(contribution_type, contribution_id):
    return contribution_type + '/' + str(contribution_id)

def get_filtered_contributions(filter_args):
    return [{'type': 'edit', 'id': x.pk, 'contribution': x} for x in EditVoyageContribution.objects.filter(**filter_args)] +\
            [{'type': 'merge', 'id': x.pk, 'contribution': x} for x in MergeVoyagesContribution.objects.filter(**filter_args)] +\
            [{'type': 'delete', 'id': x.pk, 'contribution': x} for x in DeleteVoyageContribution.objects.filter(**filter_args)] +\
            [{'type': 'new', 'id': x.pk, 'contribution': x} for x in NewVoyageContribution.objects.filter(**filter_args)]

def index(request):
    """
    Handles the redirection when user attempts to login
    Display the user index page if the user is already authenticated
    Or return to the login page if the user has not logged in yet
    """
    if request.user.is_authenticated():
        filter_args = {'contributor': request.user, 'status__lte': ContributionStatus.committed}
        contributions = get_filtered_contributions(filter_args)
        review_requests = ReviewRequest.objects.filter(
            suggested_reviewer = request.user, response__lte = 1, archived = False, final_decision = 0)
        return render(
            request, "contribute/index.html",
            {'contributions': contributions, 'review_requests': review_requests})
    else:
        return HttpResponseRedirect(reverse('account_login'))

def legal(request):
    from forms import legal_terms_title
    from forms import legal_terms_paragraph
    return render(request, 'contribute/legal.html',
                  {'title': legal_terms_title, 'paragraph': legal_terms_paragraph})

def get_summary(v):
    dates = v.voyage_dates
    return {'voyage_id': v.voyage_id,
            'captain': ', '.join([c.name for c in v.voyage_captain.all()]),
            'ship': v.voyage_ship.ship_name,
            'year_arrived': dates.get_date_year(dates.first_dis_of_slaves) or
                            dates.get_date_year(dates.imp_arrival_at_port_of_dis)}

@csrf_exempt
def get_voyage_by_id(request):
    if request.method == 'POST':
        voyage_id = request.POST.get('voyage_id')
        if voyage_id is not None:
            v = Voyage.objects.filter(voyage_id=int(voyage_id)).first()
            if v is not None:
                return JsonResponse(get_summary(v))
            else:
                error = 'No voyage found with voyage_id = ' + str(voyage_id)
        else:
            error = 'Missing voyage_id field in POST'
    else:
        error = 'POST request required'
    return JsonResponse({'error': error})

@cache_page(24 * 60 * 60)
@csrf_exempt
def get_places(request):
    # retrieve list of places in the system.
    places = sorted(Place.objects.prefetch_related('region__broad_region'),
                    key=lambda p: (
                        p.region.broad_region.broad_region if p.region.broad_region.value != 80000 else 'zzz',
                        p.region.value,
                        p.value))
    result = []
    last_broad_region = None
    last_region = None
    counter = 0
    for place in places:
        region = place.region
        broad_region = region.broad_region
        counter += 1
        if last_broad_region != broad_region:
            last_broad_region = broad_region
            result.append({'type': 'broad_region',
                           'order': counter,
                           'pk': broad_region.pk,
                           'value': -counter,
                           'broad_region': _(broad_region.broad_region)})
            counter += 1
        if last_region != region:
            last_region = region
            result.append({'type': 'region',
                           'order': counter,
                           'value': -counter,
                           'pk': region.pk,
                           'code': region.value,
                           'parent': broad_region.pk,
                           'region': _(region.region)})
            counter += 1
        result.append({'type': 'port',
                       'order': counter,
                       'value': place.pk,
                       'parent': region.pk,
                       'code': place.value,
                       'port': _(place.place)})
    return JsonResponse(result, safe=False)

@login_required
def delete(request):
    voyage_selection = []
    if request.method == 'POST':
        form = ContributionVoyageSelectionForm(request.POST)
        if form.is_valid():
            ids = form.cleaned_data['ids']
            with transaction.atomic():
                contribution = DeleteVoyageContribution()
                contribution.contributor = request.user
                contribution.status = ContributionStatus.pending
                contribution.deleted_voyages_ids = ','.join([str(x) for x in ids])
                contribution.notes = request.POST.get('notes')
                contribution.save()
            return HttpResponseRedirect(reverse('contribute:delete_review',
                                                kwargs={'contribution_id': contribution.pk}))
        else:
            ids = form.selected_voyages
            voyage_selection = [get_summary(v) for v in Voyage.objects.filter(voyage_id__in=ids)]
    else:
        form = ContributionVoyageSelectionForm()
    return render(request, 'contribute/delete.html', {
        'form': form,
        'voyage_selection': voyage_selection})

@login_required
def delete_review(request, contribution_id):
    contribution = get_object_or_404(DeleteVoyageContribution, pk=contribution_id)
    if request.user.pk != contribution.contributor.pk:
        return HttpResponseForbidden()
    if request.method == 'POST':
        action = request.POST.get('submit_val')
        if action == 'confirm':
            contribution.status = ContributionStatus.committed
            contribution.save()
            return HttpResponseRedirect(reverse('contribute:thanks'))
        elif action == 'cancel':
            contribution.delete()
            return HttpResponseRedirect(reverse('contribute:index'))
        else:
            return HttpResponseBadRequest()
    return delete_review_render(request, contribution, False, 'contributor')

def delete_review_render(request, contribution, readonly, mode):
    from voyages.apps.voyage.views import voyage_variables_data
    ids = [int(pk) for pk in contribution.deleted_voyages_ids.split(',')]
    deleted_voyage_vars = [voyage_variables_data(voyage_id, mode == 'editor')[1] for voyage_id in ids]
    review_request = None
    full_contrib_id = full_contribution_id('delete', contribution.pk)
    if mode != 'contributor':
        # Look for a review request for this delete contribution
        review_request = ReviewRequest.objects.filter(contribution_id=full_contrib_id, archived=False).first()
    return render(request, 'contribute/delete_review.html', {
        'deleted_voyage_vars': deleted_voyage_vars,
        'voyage_selection': ids,
        'readonly': readonly,
        'mode': mode,
        'review_request': review_request,
        'full_contrib_id': full_contrib_id})

@login_required
def edit(request):
    voyage_selection = []
    if request.method == 'POST':
        form = ContributionVoyageSelectionForm(request.POST, max_selection=1)
        if form.is_valid():
            ids = form.cleaned_data['ids']
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
            voyage_selection = [get_summary(v) for v in Voyage.objects.filter(voyage_id=ids[0])] \
                if len(ids) != 0 else []
    else:
        form = ContributionVoyageSelectionForm(max_selection=1)
    return render(request, 'contribute/edit.html', {'form': form, 'voyage_selection': voyage_selection})

@login_required
def merge(request):
    voyage_selection = []
    if request.method == 'POST':
        form = ContributionVoyageSelectionForm(request.POST, min_selection=2)
        if form.is_valid():
            ids = form.cleaned_data['ids']
            with transaction.atomic():
                interim_voyage = InterimVoyage()
                interim_voyage.save()
                contribution = MergeVoyagesContribution()
                contribution.interim_voyage = interim_voyage
                contribution.contributor = request.user
                contribution.merged_voyages_ids = ','.join([str(x) for x in ids])
                contribution.status = ContributionStatus.pending
                contribution.save()
                init_interim_voyage(interim_voyage, contribution)
            return HttpResponseRedirect(reverse(
                'contribute:interim', kwargs={'contribution_type': 'merge', 'contribution_id': contribution.pk}
            ))
        else:
            ids = form.selected_voyages
            voyage_selection = [get_summary(v) for v in Voyage.objects.filter(voyage_id__in=ids)]
    else:
        form = ContributionVoyageSelectionForm(min_selection=2)
    return render(request, 'contribute/merge.html', {'form': form, 'voyage_selection': voyage_selection})

def create_source(source_values, interim_voyage):
    type = source_values['type']
    source = None
    if type == 'Primary source':
        source = InterimPrimarySource()
    elif type == 'Article source':
        source = InterimArticleSource()
    elif type == 'Book source':
        source = InterimBookSource()
    elif type == 'Other source':
        source = InterimOtherSource()
    if source is None:
        raise Exception('Unrecognized source type: ' + type)
    for k, v in source_values.items():
        if hasattr(source, k):
            setattr(source, k, v if v != '' else None)
    source.interim_voyage = interim_voyage
    return source

contribution_model_by_type = {
    'delete': DeleteVoyageContribution,
    'edit': EditVoyageContribution,
    'merge': MergeVoyagesContribution,
    'new': NewVoyageContribution,
    'review': ReviewVoyageContribution,
    'editorial_review': EditorVoyageContribution
}

def get_contribution(contribution_type, contribution_id):
    model = contribution_model_by_type.get(contribution_type)
    if model is None:
        raise Http404
    contribution = get_object_or_404(model, pk=contribution_id)
    return contribution

def interim_main(request, contribution, interim):
    """
    The reusable part of the interim form handling.
    This function should be used in the views targeted at
    contributor, reviewer, and editor.
    :param request: the request which may contain interim form POST data.
    :param contribution: the contribution object, which may be a review.
    :param interim: the interim voyage data.
    :return: (Boolean b, numbers, form)
    First entry of tuple is True if GET request or valid POST, False otherwise.
    Numbers: dictionary of slave numbers
    Form: the interim form.
    """
    result = True
    if request.method == 'POST':
        form = InterimVoyageForm(request.POST, instance=interim)
        prefix = 'interim_slave_number_'
        numbers = {k: float(v) for k, v in request.POST.items() if k.startswith(prefix) and v != ''}
        sources_post = request.POST.get('sources')
        sources = [create_source(x, interim)
                   for x in json.loads(sources_post if sources_post is not None else '[]')]
        result = form.is_valid()
        if result:
            with transaction.atomic():
                def del_children(child_model):
                    child_model.objects.filter(interim_voyage__id=interim.pk).delete()
                del_children(InterimPrimarySource)
                del_children(InterimArticleSource)
                del_children(InterimBookSource)
                del_children(InterimOtherSource)
                del_children(InterimSlaveNumber)
                # Get pre-existing sources.
                for src in interim.pre_existing_sources.all():
                    src.action = request.POST.get('pre_existing_source_action_' + str(src.pk), 0)
                    src.notes = request.POST.get('pre_existing_source_notes_' + str(src.pk), '')
                    src.save()
                form.save()
                contribution.notes = request.POST.get('contribution_main_notes')
                contribution.save()
                for src in sources:
                    src.save()
                # Clear previous numbers and save new ones.
                for k, v in numbers.items():
                    number = InterimSlaveNumber()
                    number.interim_voyage = interim
                    number.var_name = k[len(prefix):]
                    number.number = v
                    number.save()
    else:
        numbers = {number_prefix + n.var_name: n.number for n in interim.slave_numbers.all()}
        form = InterimVoyageForm(instance=interim)
    return result, form, numbers

@login_required
def interim(request, contribution_type, contribution_id):
    if contribution_type == 'delete':
        return HttpResponseRedirect(reverse('contribute:delete_review',
                                    kwargs={'contribution_id': contribution_id}))

    contribution = get_contribution(contribution_type, contribution_id)
    if request.user.pk != contribution.contributor.pk:
        return HttpResponseForbidden()

    def redirect():
        return HttpResponseRedirect(reverse(
            'contribute:interim_summary',
            kwargs={'contribution_type': contribution_type, 'contribution_id': contribution_id}))

    if request.GET.get('revert_to_pending') == 'true' and contribution.status <= ContributionStatus.committed:
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
    (valid, form, numbers) = interim_main(request, contribution, interim)
    if valid and request.method == 'POST':
        return redirect()
    sources_post = None if request.method != 'POST' else request.POST.get('sources')
    previous_data = contribution_related_data(contribution)
    return render(request, 'contribute/interim.html',
                  {'form': form,
                   'mode': 'contribute',
                   'contribution': contribution,
                   'numbers': numbers,
                   'interim': interim,
                   'sources_post': sources_post,
                   'voyages_data': json.dumps(previous_data)})

def common_save_ajax(request, contribution):
    (valid, form, numbers) = interim_main(request, contribution, contribution.interim_voyage)
    return JsonResponse({'valid': valid, 'errors': form.errors})
    
@login_required
@require_POST
def interim_save_ajax(request, contribution_type, contribution_id):
    contribution = get_contribution(contribution_type, contribution_id)
    if request.user.pk != contribution.contributor.pk:
        return HttpResponseForbidden()
    return common_save_ajax(request, contribution)
    
@login_required
@require_POST
def editorial_review_interim_save_ajax(request, editor_contribution_id):
    contribution = get_object_or_404(EditorVoyageContribution, pk=editor_contribution_id)
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    return common_save_ajax(request, contribution)

@login_required
@require_POST
def review_interim_save_ajax(request, review_request_id):
    review_request = get_object_or_404(ReviewRequest, pk=review_request_id)
    if request.user.pk != review_request.suggested_reviewer.pk:
        return HttpResponseForbidden()
    return common_save_ajax(request, review_request.review_contribution.first())

@login_required
def interim_commit(request, contribution_type, contribution_id):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    contribution = get_contribution(contribution_type, contribution_id)
    if request.user.pk != contribution.contributor.pk or contribution.status != ContributionStatus.pending:
        return HttpResponseForbidden()
    contribution.status = ContributionStatus.committed
    contribution.save()
    return HttpResponseRedirect(reverse('contribute:thanks'))

@login_required()
def interim_summary(request, contribution_type, contribution_id, mode='contribute'):
    contribution = get_contribution(contribution_type, contribution_id)
    if not request.user.is_superuser and request.user.pk != contribution.contributor.pk:
        return HttpResponseForbidden()
    if contribution_type == 'delete':
        return delete_review_render(request, contribution, True, 'editor')
    numbers = {number_prefix + n.var_name: n.number for n in contribution.interim_voyage.slave_numbers.all()}
    form = InterimVoyageForm(instance=contribution.interim_voyage)
    previous_data = contribution_related_data(contribution)
    full_contrib_id = full_contribution_id(contribution_type, contribution_id)
    reqs = list(ReviewRequest.objects.filter(contribution_id=full_contrib_id, archived=False))
    if len(reqs) > 1:
        raise Exception('Invalid state: more than one review request is active')
    return render(request, 'contribute/interim_summary.html',
                  {'contribution': contribution,
                   'review_request': reqs[0] if len(reqs) == 1 else None,
                   'full_contrib_id': full_contrib_id,
                   'interim': contribution.interim_voyage,
                   'mode': mode,
                   'numbers': numbers,
                   'form': form,
                   'user': request.user,
                   'voyages_data': json.dumps(previous_data)})

@login_required
def new_voyage(request):
    interim_voyage = InterimVoyage()
    interim_voyage.save()
    contrib = NewVoyageContribution()
    contrib.contributor = request.user
    contrib.interim_voyage = interim_voyage
    contrib.status = ContributionStatus.pending
    contrib.save()
    return HttpResponseRedirect(reverse(
        'contribute:interim', kwargs={'contribution_type': 'new', 'contribution_id': contrib.pk}))

def init_interim_voyage(interim, contribution):
    # If this is a merger or edit, initialize fields when there is consensus.
    previous_data = contribution_related_data(contribution)
    if len(previous_data) > 0:
        values = previous_data.values()
        for k, v in values[0].items():
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
    for tuples in source_to_voyage.values():
        conn = tuples[0][1]
        ps = InterimPreExistingSource()
        ps.interim_voyage = interim
        ps.voyage_ids = ','.join([str(v.voyage_id) for (v, c) in tuples])
        ps.original_ref = conn.text_ref
        ps.full_ref = conn.source.full_ref
        ps.save()

def contribution_related_data(contribution):    
    previous_data = {}
    related = contribution.get_related_voyages()
    for voyage in related:
        previous_data[voyage.voyage_id] = voyage_to_dict(voyage)
    return previous_data

def voyage_to_dict(voyage):
    dict = {}
    # Ship, nation, owners
    VoyageCache.load()
    ship = voyage.voyage_ship

    def get_label(obj, field='name'):
        if obj is None:
            return None
        return getattr(obj, field)
    if ship is not None:
        dict['name_of_vessel'] = ship.ship_name
        dict['year_ship_constructed'] = ship.year_of_construction
        dict['year_ship_registered'] = ship.registered_year
        dict['national_carrier'] = ship.nationality_ship_id
        dict['national_carrier_name'] = VoyageCache.nations.get(ship.nationality_ship_id)
        dict['ship_construction_place'] = ship.vessel_construction_place_id
        dict['ship_construction_place_name'] = get_label(VoyageCache.ports.get(ship.vessel_construction_place_id))
        dict['ship_registration_place'] = ship.registered_place_id
        dict['ship_registration_place_name'] = get_label(VoyageCache.ports.get(ship.registered_place_id))
        dict['rig_of_vessel'] = ship.rig_of_vessel_id
        dict['rig_of_vessel_name'] = get_label(VoyageCache.rigs.get(ship.rig_of_vessel_id), 'label')
        dict['tonnage_of_vessel'] = ship.tonnage
        dict['ton_type'] = ship.ton_type_id
        dict['ton_type_name'] = get_label(VoyageCache.ton_types.get(ship.ton_type_id), 'label')
        dict['guns_mounted'] = ship.guns_mounted
        owners = list(VoyageShipOwnerConnection.objects.filter(voyage=voyage).extra(order_by=['owner_order']))
        if len(owners) > 0:
            dict['first_ship_owner'] = owners[0].owner.name
        if len(owners) > 1:
            dict['second_ship_owner'] = owners[1].owner.name
        if len(owners) > 2:
            dict['additional_ship_owners'] = '\n'.join([x.owner.name for x in owners[2:]])
    # Outcome
    outcome = voyage.voyage_name_outcome.get()
    if outcome is not None:
        dict['voyage_outcome'] = outcome.particular_outcome_id
        dict['african_resistance'] = outcome.resistance_id
        dict['voyage_outcome_name'] = get_label(
            VoyageCache.particular_outcomes.get(outcome.particular_outcome_id), 'label')
        dict['african_resistance_name'] = get_label(VoyageCache.resistances.get(outcome.resistance_id), 'label')
    itinerary = voyage.voyage_itinerary
    if itinerary is not None:
        dict['first_port_intended_embarkation'] = itinerary.int_first_port_emb_id
        dict['second_port_intended_embarkation'] = itinerary.int_second_port_emb_id
        dict['first_port_intended_disembarkation'] = itinerary.int_first_port_dis_id
        dict['second_port_intended_disembarkation'] = itinerary.int_second_port_dis_id
        dict['port_of_departure'] = itinerary.port_of_departure_id
        dict['number_of_ports_called_prior_to_slave_purchase'] = itinerary.ports_called_buying_slaves
        dict['first_place_of_slave_purchase'] = itinerary.first_place_slave_purchase_id
        dict['second_place_of_slave_purchase'] = itinerary.second_place_slave_purchase_id
        dict['third_place_of_slave_purchase'] = itinerary.third_place_slave_purchase_id
        dict['principal_place_of_slave_purchase'] = itinerary.principal_place_of_slave_purchase_id
        dict['place_of_call_before_atlantic_crossing'] = itinerary.port_of_call_before_atl_crossing_id
        dict['number_of_new_world_ports_called_prior_to_disembarkation'] = itinerary.number_of_ports_of_call
        dict['first_place_of_landing'] = itinerary.first_landing_place_id
        dict['second_place_of_landing'] = itinerary.second_landing_place_id
        dict['third_place_of_landing'] = itinerary.third_landing_place_id
        dict['principal_place_of_slave_disembarkation'] = itinerary.principal_port_of_slave_dis_id
        dict['port_voyage_ended'] = itinerary.place_voyage_ended_id
        # Port names.
        dict['first_port_intended_embarkation_name'] = get_label(VoyageCache.ports.get(itinerary.int_first_port_emb_id))
        dict['second_port_intended_embarkation_name'] = get_label(VoyageCache.ports.get(itinerary.int_second_port_emb_id))
        dict['first_port_intended_disembarkation_name'] = get_label(VoyageCache.ports.get(itinerary.int_first_port_dis_id))
        dict['second_port_intended_disembarkation_name'] = get_label(VoyageCache.ports.get(itinerary.int_second_port_dis_id))
        dict['port_of_departure_name'] = get_label(VoyageCache.ports.get(itinerary.port_of_departure_id))
        dict['first_place_of_slave_purchase_name'] = get_label(VoyageCache.ports.get(itinerary.first_place_slave_purchase_id))
        dict['second_place_of_slave_purchase_name'] = get_label(VoyageCache.ports.get(itinerary.second_place_slave_purchase_id))
        dict['third_place_of_slave_purchase_name'] = get_label(VoyageCache.ports.get(itinerary.third_place_slave_purchase_id))
        dict['principal_place_of_slave_purchase_name'] = get_label(VoyageCache.ports.get(itinerary.principal_place_of_slave_purchase_id))
        dict['place_of_call_before_atlantic_crossing_name'] = get_label(VoyageCache.ports.get(itinerary.port_of_call_before_atl_crossing_id))
        dict['first_place_of_landing_name'] = get_label(VoyageCache.ports.get(itinerary.first_landing_place_id))
        dict['second_place_of_landing_name'] = get_label(VoyageCache.ports.get(itinerary.second_landing_place_id))
        dict['third_place_of_landing_name'] = get_label(VoyageCache.ports.get(itinerary.third_landing_place_id))
        dict['principal_place_of_slave_disembarkation_name'] = get_label(VoyageCache.ports.get(itinerary.principal_port_of_slave_dis_id))
        dict['port_voyage_ended_name'] = get_label(VoyageCache.ports.get(itinerary.place_voyage_ended_id))
    dates = voyage.voyage_dates
    if dates is not None:
        dict['date_departure'] = dates.voyage_began
        dict['date_slave_purchase_began'] = dates.slave_purchase_began
        dict['date_vessel_left_last_slaving_port'] = dates.vessel_left_port
        dict['date_first_slave_disembarkation'] = dates.first_dis_of_slaves
        dict['date_second_slave_disembarkation'] = dates.arrival_at_second_place_landing
        dict['date_third_slave_disembarkation'] = dates.third_dis_of_slaves
        dict['date_return_departure'] = dates.departure_last_place_of_landing
        dict['date_voyage_completed'] = dates.voyage_completed
        dict['length_of_middle_passage'] = dates.length_middle_passage_days
    numbers = voyage.voyage_slaves_numbers
    if numbers is not None:
        dict[number_prefix + 'SLADAFRI'] = numbers.slave_deaths_before_africa
        dict[number_prefix + 'SLADVOY'] = numbers.slave_deaths_between_africa_america
        dict[number_prefix + 'SLADAMER'] = numbers.slave_deaths_between_arrival_and_sale
        dict[number_prefix + 'SLINTEND'] = numbers.num_slaves_intended_first_port
        dict[number_prefix + 'SLINTEN2'] = numbers.num_slaves_intended_second_port
        dict[number_prefix + 'NCAR13'] = numbers.num_slaves_carried_first_port
        dict[number_prefix + 'NCAR15'] = numbers.num_slaves_carried_second_port
        dict[number_prefix + 'NCAR17'] = numbers.num_slaves_carried_third_port
        dict[number_prefix + 'TSLAVESP'] = numbers.total_num_slaves_purchased
        dict[number_prefix + 'TSLAVESD'] = numbers.total_num_slaves_dep_last_slaving_port
        dict[number_prefix + 'SLAARRIV'] = numbers.total_num_slaves_arr_first_port_embark
        dict[number_prefix + 'SLAS32'] = numbers.num_slaves_disembark_first_place
        dict[number_prefix + 'SLAS36'] = numbers.num_slaves_disembark_second_place
        dict[number_prefix + 'SLAS39'] = numbers.num_slaves_disembark_third_place
        # Demographics
        dict[number_prefix + 'MEN1'] = numbers.num_men_embark_first_port_purchase
        dict[number_prefix + 'WOMEN1'] = numbers.num_women_embark_first_port_purchase
        dict[number_prefix + 'BOY1'] = numbers.num_boy_embark_first_port_purchase
        dict[number_prefix + 'GIRL1'] = numbers.num_girl_embark_first_port_purchase
        dict[number_prefix + 'ADULT1'] = numbers.num_adult_embark_first_port_purchase
        dict[number_prefix + 'CHILD1'] = numbers.num_child_embark_first_port_purchase
        dict[number_prefix + 'INFANT1'] = numbers.num_infant_embark_first_port_purchase
        dict[number_prefix + 'MALE1'] = numbers.num_males_embark_first_port_purchase
        dict[number_prefix + 'FEMALE1'] = numbers.num_females_embark_first_port_purchase
        dict[number_prefix + 'MEN2'] = numbers.num_men_died_middle_passage
        dict[number_prefix + 'WOMEN2'] = numbers.num_women_died_middle_passage
        dict[number_prefix + 'BOY2'] = numbers.num_boy_died_middle_passage
        dict[number_prefix + 'GIRL2'] = numbers.num_girl_died_middle_passage
        dict[number_prefix + 'ADULT2'] = numbers.num_adult_died_middle_passage
        dict[number_prefix + 'CHILD2'] = numbers.num_child_died_middle_passage
        dict[number_prefix + 'INFANT2'] = numbers.num_infant_died_middle_passage
        dict[number_prefix + 'MALE2'] = numbers.num_males_died_middle_passage
        dict[number_prefix + 'FEMALE2'] = numbers.num_females_died_middle_passage
        dict[number_prefix + 'MEN3'] = numbers.num_men_disembark_first_landing
        dict[number_prefix + 'WOMEN3'] = numbers.num_women_disembark_first_landing
        dict[number_prefix + 'BOY3'] = numbers.num_boy_disembark_first_landing
        dict[number_prefix + 'GIRL3'] = numbers.num_girl_disembark_first_landing
        dict[number_prefix + 'ADULT3'] = numbers.num_adult_disembark_first_landing
        dict[number_prefix + 'CHILD3'] = numbers.num_child_disembark_first_landing
        dict[number_prefix + 'INFANT3'] = numbers.num_infant_disembark_first_landing
        dict[number_prefix + 'MALE3'] = numbers.num_males_disembark_first_landing
        dict[number_prefix + 'FEMALE3'] = numbers.num_females_disembark_first_landing
        dict[number_prefix + 'MEN4'] = numbers.num_men_embark_second_port_purchase
        dict[number_prefix + 'WOMEN4'] = numbers.num_women_embark_second_port_purchase
        dict[number_prefix + 'BOY4'] = numbers.num_boy_embark_second_port_purchase
        dict[number_prefix + 'GIRL4'] = numbers.num_girl_embark_second_port_purchase
        dict[number_prefix + 'ADULT4'] = numbers.num_adult_embark_second_port_purchase
        dict[number_prefix + 'CHILD4'] = numbers.num_child_embark_second_port_purchase
        dict[number_prefix + 'INFANT4'] = numbers.num_infant_embark_second_port_purchase
        dict[number_prefix + 'MALE4'] = numbers.num_males_embark_second_port_purchase
        dict[number_prefix + 'FEMALE4'] = numbers.num_females_embark_second_port_purchase
        dict[number_prefix + 'MEN5'] = numbers.num_men_embark_third_port_purchase
        dict[number_prefix + 'WOMEN5'] = numbers.num_women_embark_third_port_purchase
        dict[number_prefix + 'BOY5'] = numbers.num_boy_embark_third_port_purchase
        dict[number_prefix + 'GIRL5'] = numbers.num_girl_embark_third_port_purchase
        dict[number_prefix + 'ADULT5'] = numbers.num_adult_embark_third_port_purchase
        dict[number_prefix + 'CHILD5'] = numbers.num_child_embark_third_port_purchase
        dict[number_prefix + 'INFANT5'] = numbers.num_infant_embark_third_port_purchase
        dict[number_prefix + 'MALE5'] = numbers.num_males_embark_third_port_purchase
        dict[number_prefix + 'FEMALE5'] = numbers.num_females_embark_third_port_purchase
        dict[number_prefix + 'MEN6'] = numbers.num_men_disembark_second_landing
        dict[number_prefix + 'WOMEN6'] = numbers.num_women_disembark_second_landing
        dict[number_prefix + 'BOY6'] = numbers.num_boy_disembark_second_landing
        dict[number_prefix + 'GIRL6'] = numbers.num_girl_disembark_second_landing
        dict[number_prefix + 'ADULT6'] = numbers.num_adult_disembark_second_landing
        dict[number_prefix + 'CHILD6'] = numbers.num_child_disembark_second_landing
        dict[number_prefix + 'INFANT6'] = numbers.num_infant_disembark_second_landing
        dict[number_prefix + 'MALE6'] = numbers.num_males_disembark_second_landing
        dict[number_prefix + 'FEMALE6'] = numbers.num_females_disembark_second_landing

    # Captains
    captains = voyage.voyage_captain.all()
    captain_keys = ['first', 'second', 'third']
    for i in range(0, len(captains)):
        dict[captain_keys[i] + '_captain'] = captains[i].name
    # Crew numbers
    crew = voyage.voyage_crew
    if crew is not None:
        dict[number_prefix + 'CREW1'] = crew.crew_voyage_outset
        dict[number_prefix + 'CREW2'] = crew.crew_departure_last_port
        dict[number_prefix + 'CREW3'] = crew.crew_first_landing
        dict[number_prefix + 'CREW4'] = crew.crew_return_begin
        dict[number_prefix + 'CREW5'] = crew.crew_end_voyage
        dict[number_prefix + 'CREW'] = crew.unspecified_crew
        dict[number_prefix + 'SAILD1'] = crew.crew_died_before_first_trade
        dict[number_prefix + 'SAILD2'] = crew.crew_died_while_ship_african
        dict[number_prefix + 'SAILD3'] = crew.crew_died_middle_passage
        dict[number_prefix + 'SAILD4'] = crew.crew_died_in_americas
        dict[number_prefix + 'SAILD5'] = crew.crew_died_on_return_voyage
        dict[number_prefix + 'CREWDIED'] = crew.crew_died_complete_voyage
        dict[number_prefix + 'NDESERT'] = crew.crew_deserted
    return dict

@login_required()
def editor_main(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    return render(request, 'contribute/editor_main.html')

@login_required()
def get_pending_requests(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    filter_args = {'status__in': ContributionStatus.active_statuses}
    contributions = get_filtered_contributions(filter_args)
    
    def get_contribution_info(info):
        contrib = info['contribution']
        voyage_ids = contrib.get_related_voyage_ids()
        voyage_info = [unicode(v.voyage_ship.ship_name) + u' (' + unicode(VoyageDates.get_date_year(v.voyage_dates.voyage_began)) + ')'
                       for v in Voyage.objects.filter(voyage_id__in=voyage_ids)]
        res = {'type': info['type'],
               'id': info['id'],
               'contributor': contrib.contributor.get_full_name(),
               'date_created': contrib.date_created,
               'voyage_ids': voyage_ids,
               'voyage_info': voyage_info}
        # Fetch review info.
        reqs = list(ReviewRequest.objects.filter(contribution_id=full_contribution_id(info['type'], info['id']), archived=False))
        if len(reqs) > 1:
            raise Exception('Invalid state: more than one review request is active')
        if len(reqs) == 1:
            active_request = reqs[0]
            res['review_request_id'] = active_request.pk
            res['reviewer'] = active_request.suggested_reviewer.get_full_name()
            res['response_id'] = active_request.response
            res['response'] = active_request.get_status_msg() \
                if active_request.final_decision in [ReviewRequestDecision.under_review, ReviewRequestDecision.begun_editorial_review] else _('Reviewer decision posted')
            res['reviewer_comments'] = active_request.reviewer_comments
            res['reviewer_final_decision'] = active_request.get_status_msg()
            if active_request.final_decision:
                # Fetch if of the editor's contribution.
                res['editor_contribution_id'] = active_request.editor_contribution.first().pk
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

    return JsonResponse({full_contribution_id(x['type'], x['id']): get_contribution_info(x) for x in contributions})

def get_reviewers(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    reviewers = [{'full_name': u.get_full_name(), 'pk': u.pk} for u in User.objects.filter(is_staff=True)]
    return JsonResponse(reviewers, safe=False)

def get_contribution_from_id(contribution_id):
    if contribution_id is None:
        return None
    contribution_pair = contribution_id.split('/')
    contribution_type = contribution_pair[0]
    contribution_id = int(contribution_pair[1])
    return get_contribution(contribution_type, contribution_id)

def assert_no_active_review_requests(contribution_id):
    reqs = [req for req in ReviewRequest.objects.filter(contribution_id=contribution_id) if not req.archived]
    if len(reqs) >= 1:
        return JsonResponse({'error': _('There is already an active review for this contribution')})
    return None
        
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
    assertion = assert_no_active_review_requests(contribution_id)
    if assertion: return assertion    
    review_request = ReviewRequest()
    with transaction.atomic():
        reviewer = request.user
        review_request.editor = request.user
        review_request.editor_comments = 'Editorial review bypassing a reviewer'
        review_request.email_sent = False
        review_request.contribution_id = contribution_id
        review_request.suggested_reviewer = reviewer
        review_request.response = ReviewRequestResponse.begun_editorial_review
        review_request.final_decision = ReviewRequestDecision.begun_editorial_review
        review_request.save()
        contribution.status = ContributionStatus.under_review
        contribution.save()
        contributor_prefix = 'Contributor: '
        editor_contribution = EditorVoyageContribution()
        editor_contribution.request = review_request
        editor_contribution.notes = contributor_prefix + contribution.notes if contribution.notes else ''
        if hasattr(contribution, 'interim_voyage'):
            editor_contribution.interim_voyage = clone_interim_voyage(contribution, contributor_prefix)
        editor_contribution.save()
        editor_contribution_id = editor_contribution.pk
    return JsonResponse({'review_request_id': review_request.pk, 'editor_contribution_id': editor_contribution_id})

@login_required()
@require_POST
def post_review_request(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    contribution_id = request.POST.get('contribution_id')
    contribution = get_contribution_from_id(contribution_id)
    reviewer_id = int(request.POST.get('reviewer_id'))
    message = request.POST.get('message')
    if contribution.contributor_id == reviewer_id:
        return JsonResponse({'error': _('Reviewer and contributor must be different users')})
    
    if request.POST.get('archive_active_requests') == True:
        ReviewRequest.objects.filter(contribution_id=contribution_id, archived=False).update(archived=True)
    else:
        assertion = assert_no_active_review_requests(contribution_id)
        if assertion: return assertion

    review_request = ReviewRequest()
    try:
        with transaction.atomic():
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
        reply_url = settings.WEBSITE_ROOT + '/contribute/reply_review_request/' + str(review_request.pk)
        result = send_mail(
            'Voyages - contribution review request',
            'Editor message:\r\n' + message + '\n\nPlease visit ' + reply_url + '\r\nto reply.',
            settings.CONTRIBUTE_SENDER_EMAIL,
            [reviewer.email],
            html_message='<strong>Editor message:</strong><p>' + message + '</p>' + '<p>Please click <a href="' + reply_url + '">here</a> to reply.</p>')
    except Exception as e:
        print e
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
    reqs = [req for req in ReviewRequest.objects.filter(contribution_id=contribution_id)
            if not req.archived]
    if len(reqs) == 0:
        return JsonResponse({'error': _('There is no active review for this contribution')})
    for req in reqs:
        req.archived = True
        req.save()
    return JsonResponse({'result': len(reqs)})

@login_required()
def review_request(request, review_request_id):
    req = get_object_or_404(ReviewRequest, pk=review_request_id)
    if req.archived or req.suggested_reviewer_id != request.user.pk:
        return HttpResponseForbidden()
    if req.review_contribution.first():
        return HttpResponseRedirect(reverse('contribute:review', kwargs={'review_request_id': review_request_id}))
    contribution = get_contribution_from_id(req.contribution_id)
    if contribution is None:
        raise Http404
    return render(request, 'contribute/review_request.html', {'request': req, 'contribution': contribution})

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
    related_models = list(interim.article_sources.all()) + list(interim.book_sources.all()) + \
                        list(interim.other_sources.all()) + list(interim.primary_sources.all()) + \
                        list(interim.pre_existing_sources.all()) + list(interim.slave_numbers.all())
    interim.pk = None
    # Prepend comments with contributor name.
    changed = {}
    try:
        note_dict = json.loads(interim.notes) if interim.notes else {}
    except:
        note_dict = {'parse_error': interim.notes}
    for key, note in note_dict.items():
        changed[key] = contributor_comment_prefix + note
        
    with transaction.atomic():
        interim.notes = json.dumps(changed)
        interim.save()
        for item in related_models:
            item.pk = None
            item.interim_voyage = interim
            if hasattr(item, 'notes') and item.notes is not None and item.notes != '':
                item.notes = contributor_comment_prefix + item.notes
            item.save()
        return interim

@login_required()
@require_POST
def reply_review_request(request):
    review_request_id = request.POST.get('review_request_id')
    req = get_object_or_404(ReviewRequest, pk=review_request_id)

    if req.suggested_reviewer_id != request.user.pk:
        return HttpResponseForbidden()

    redirect = HttpResponseRedirect(reverse('contribute:review', kwargs={'review_request_id': review_request_id}))
    if req.review_contribution.count() > 0:
        return redirect

    # Check response
    response = request.POST.get('response')
    valid_responses = ['accept', 'reject']
    if response not in valid_responses:
        return HttpResponseBadRequest()
    req.response = ReviewRequestResponse.accepted if response == 'accept' else ReviewRequestResponse.rejected
    req.reviewer_comments = request.POST.get('message_to_editor')
    with transaction.atomic():
        req.save()
        if response == 'accept':
            review = ReviewVoyageContribution()
            review.request = req
            contribution = get_contribution_from_id(req.contribution_id)
            if hasattr(contribution, 'interim_voyage'):
                review.interim_voyage = clone_interim_voyage(contribution, 'Contributor: ')
            review.notes = 'Contributor: ' + contribution.notes if contribution.notes else ''
            review.save()
        else:
            redirect = HttpResponseRedirect(reverse('contribute:index'))
    return redirect

def interim_data(interim):
    from django.db.models.fields import Field
    dict = {number_prefix + n.var_name: n.number for n in interim.slave_numbers.all() if n.number is not None}
    fields = [f for f in InterimVoyage._meta.get_fields() if isinstance(f, Field)]
    for field in fields:
        # Check if this is a foreign key.
        name = field.name
        value = getattr(interim, field.name)
        if value is None:
            continue
        type = field.get_internal_type()
        if type == 'ForeignKey':
            try:
                dict[name] = value.pk
                dict[name + 'name'] = str(value)
            except:
                pass
        elif type in ['IntegerField', 'CharField', 'TextField', 'CommaSeparatedIntegerField']:
            if value != '':
                dict[name] = value
    return dict

@login_required()
def review(request, review_request_id):
    req = get_object_or_404(ReviewRequest, pk=review_request_id)
    if req.archived or req.response == 2 or req.final_decision != 0 or req.suggested_reviewer_id != request.user.pk:
        return HttpResponseForbidden()
    if req.response == 0:
        return HttpResponseRedirect(reverse('contribute:review_request',
                                            kwargs={'review_request_id': review_request_id}))
    contribution_id = req.contribution_id
    user_contribution = get_contribution_from_id(contribution_id)
    if contribution_id.startswith('delete'):
        return delete_review_render(request, user_contribution, True, 'reviewer')
    review_contribution = req.review_contribution.first()
    interim = review_contribution.interim_voyage if review_contribution else None
    if interim is None:
        raise Exception('Could not find reviewer\'s interim form')
    (result, form, numbers) = interim_main(request, review_contribution, interim)
    sources_post = None if request.method != 'POST' else request.POST.get('sources')
    # Build previous data dictionary.
    # For the review we need to include both the original voyage(s) data
    # as well as the user contribution itself.
    previous_data = contribution_related_data(user_contribution)
    previous_data[_('User contribution')] = interim_data(user_contribution.interim_voyage)
    return render(request, 'contribute/interim.html',
                  {'form': form,
                   'mode': 'review',
                   'contribution': review_contribution,
                   'numbers': numbers,
                   'interim': interim,
                   'sources_post': sources_post,
                   'voyages_data': json.dumps(previous_data)})

@login_required()
def editorial_review(request, review_request_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    review_request = get_object_or_404(ReviewRequest, pk=review_request_id)
    contribution = review_request.editor_contribution.first()
    contribution_id = review_request.contribution_id    
    user_contribution = get_contribution_from_id(contribution_id)
    if contribution_id.startswith('delete'):
        return delete_review_render(request, user_contribution, True, 'editor')
    review_contribution = review_request.review_contribution.first()
    reviewer_interim = review_contribution.interim_voyage if review_contribution else None
    sources_post = None if request.method != 'POST' else request.POST.get('sources')
    # Build previous data dictionary.
    # Include pre-existing voyage data, user contribution, and reviewer version.
    previous_data = contribution_related_data(user_contribution)
    previous_data[_('User contribution')] = interim_data(user_contribution.interim_voyage)
    if reviewer_interim:
        previous_data[_('Reviewer')] = interim_data(reviewer_interim)
    editor_interim = contribution.interim_voyage
    (result, form, numbers) = interim_main(request, contribution, editor_interim)
    return render(request, 'contribute/interim.html',
                  {'form': form,
                   'mode': 'editorial_review',
                   'contribution': contribution,
                   'numbers': numbers,
                   'interim': editor_interim,
                   'sources_post': sources_post,
                   'voyages_data': json.dumps(previous_data)})

@login_required()
@require_POST
def submit_editorial_decision(request, editor_contribution_id):
    contribution = get_object_or_404(EditorVoyageContribution, pk=editor_contribution_id)
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    decision = -1
    try:
        decision = int(request.POST['editorial_decision'])
    except:
        pass
    if not decision in [ReviewRequestDecision.accepted_by_editor, ReviewRequestDecision.rejected_by_editor, ReviewRequestDecision.deleted]:
        return HttpResponseBadRequest()
    with transaction.atomic():
        # Save interim form.
        if contribution.interim_voyage:
            (valid, form, numbers) = interim_main(request, contribution, contribution.interim_voyage)
            if not valid:
                return JsonResponse({'valid': valid, 'errors': form.errors})
        # Fetch decision.
        review_request = contribution.request
        review_request.final_decision = decision
        msg = request.POST.get('decision_message')
        msg = 'Editor: ' + msg if msg else ''
        review_request.decision_message = msg
        review_request.save()
        user_contribution = get_contribution_from_id(review_request.contribution_id)
        user_contribution.status = decision
        user_contribution.save()
    return JsonResponse({'result': 'OK'})
    
@login_required()
@require_POST
def submit_review_to_editor(request, review_request_id):
    req = get_object_or_404(ReviewRequest, pk=review_request_id)
    if req.archived or req.response != 1 or req.suggested_reviewer_id != request.user.pk:
        return HttpResponseForbidden()
    decision = -1
    try:
        decision = int(request.POST['reviewer_decision'])
    except:
        pass
    if decision != ReviewRequestDecision.accepted_by_reviewer and decision != ReviewRequestDecision.rejected_by_reviewer:
        return HttpResponseBadRequest()
    try:
        with transaction.atomic():
            # Save interim form.
            contribution = req.review_contribution.first()
            has_interim_voyage = hasattr(contribution, 'interim_voyage') and contribution.interim_voyage
            if has_interim_voyage:
                (valid, form, numbers) = interim_main(request, contribution, contribution.interim_voyage)
                if not valid:
                    return JsonResponse({'result': 'Failed', 'errors': form.errors})
            # Save review request with decision.
            msg = request.POST.get('message_to_editor')
            msg = 'Reviewer: ' + msg if msg else ''
            req.decision_message = msg
            req.final_decision = decision
            req.save()
            # Create an editor contribution with cloned review data.
            editor_contribution = EditorVoyageContribution()
            editor_contribution.request = req
            editor_contribution.notes = 'Reviewer: ' + contribution.notes if contribution.notes else ''            
            if has_interim_voyage:
                editor_contribution.interim_voyage = clone_interim_voyage(contribution, 'Reviewer: ')
            editor_contribution.save()
        return JsonResponse({'result': 'OK'})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'result': 'Failed', 'errors': [str(e)]})
        
@login_required()
@require_POST
def impute_contribution(request, editor_contribution_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    # First we save the current version of the interim voyage.
    contribution = get_object_or_404(EditorVoyageContribution, pk=editor_contribution_id)
    (valid, form, numbers) = interim_main(request, contribution, contribution.interim_voyage)
    if not valid:
        return JsonResponse({'result': 'Failed', 'errors': form.errors})
    interim_voyage_id = contribution.interim_voyage_id
    # Reload the interim voyage from database, just in case.
    interim = get_object_or_404(InterimVoyage, pk=interim_voyage_id)
    result = imputed.compute_imputed_vars(interim)[0]
    # Map imputed fields back to the contribution, save it and yield response.
    for k, v in result.items():
        setattr(interim, k, v)
    interim.save()
    return JsonResponse({'result': 'OK'})