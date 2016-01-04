# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from voyages.apps.contribute.forms import *
from voyages.apps.contribute.models import *
from voyages.apps.voyage.models import *
from django.utils.translation import ugettext as _

def index(request):
    """
    Handles the redirection when user attempts to login
    Display the user index page if the user is already authenticated
    Or return to the login page if the user has not logged in yet
    """
    if request.user.is_authenticated():
        contributions = [{'type': 'edit', 'id': x.pk} for x in EditVoyageContribution.objects.filter(contributor=request.user)] +\
            [{'type': 'merge', 'id': x.pk} for x in MergeVoyagesContribution.objects.filter(contributor=request.user)] +\
            [{'type': 'new', 'id': x.pk} for x in NewVoyageContribution.objects.filter(contributor=request.user)]
        return render(request, "contribute/index.html", {'contributions': contributions})
    else:
        return HttpResponseRedirect(reverse('account_login'))

def get_summary(v):
    dates = v.voyage_dates
    return {'voyage_id': v.voyage_id,
            'captain': ', '.join([c.name for c in v.voyage_captain.all()]),
            'ship': v.voyage_ship.ship_name,
            'year_arrived': dates.get_date_year(dates.first_dis_of_slaves)}

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


@csrf_exempt
def get_places(request):
    # retrieve list of places in the system.
    places = sorted(Place.objects.prefetch_related('region__broad_region'),
                    key=lambda p: (p.region.broad_region.broad_region, p.region.region, p.place))
    result = []
    last_broad_region = None
    last_region = None
    brcounter = 0
    rcounter = 0
    for place in places:
        region = place.region
        broad_region = region.broad_region
        if last_broad_region != broad_region:
            brcounter += 1
            last_broad_region = broad_region
            result.append({'type': 'broad_region',
                           'pk': broad_region.pk,
                           'value': -100000 * brcounter,
                           'broad_region': _(broad_region.broad_region)})
        if last_region != region:
            rcounter += 1
            last_region = region
            result.append({'type': 'region',
                           'value': -rcounter,
                           'pk': region.pk,
                           'parent': broad_region.pk,
                           'region': _(region.region)})
        result.append({'type': 'port',
                       'value': place.pk,
                       'parent': region.pk,
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
                contribution.deleted_voyages_ids = ','.join([str(x) for x in ids])
                contribution.status = ContributionStatus.committed
                contribution.notes = form.cleaned_data['notes']
                contribution.save()
            return HttpResponseRedirect(reverse('contribute:thanks'))
        else:
            ids = form.selected_voyages
            voyage_selection = [get_summary(v) for v in Voyage.objects.filter(voyage_id__in=ids)]
    else:
        form = ContributionVoyageSelectionForm()
    return render(request, 'contribute/delete.html', {'form': form, 'voyage_selection': voyage_selection})

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
                contribution.notes = form.cleaned_data['notes']
                contribution.save()
            return HttpResponseRedirect(reverse(
                'contribute:interim', kwargs={'contribution_type': 'edit', 'contribution_id': contribution.pk}
            ))
        else:
            ids = form.selected_voyages
            voyage_selection = [get_summary(v) for v in Voyage.objects.filter(voyage_id=ids[0])]
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
                contribution.notes = form.cleaned_data['notes']
                contribution.save()
            return HttpResponseRedirect(reverse(
                'contribute:interim', kwargs={'contribution_type': 'merge', 'contribution_id': contribution.pk}
            ))
        else:
            ids = form.selected_voyages
            voyage_selection = [get_summary(v) for v in Voyage.objects.filter(voyage_id__in=ids)]
    else:
        form = ContributionVoyageSelectionForm(min_selection=2)
    return render(request, 'contribute/merge.html', {'form': form, 'voyage_selection': voyage_selection})

contribution_model_by_type = {
    'edit': EditVoyageContribution,
    'merge': MergeVoyagesContribution,
    'new': NewVoyageContribution
}

@login_required
def interim(request, contribution_type, contribution_id):
    model = contribution_model_by_type.get(contribution_type)
    if model is None:
        raise Http404
    contribution = model.objects.get(pk=contribution_id)
    if contribution.status != ContributionStatus.pending and contribution.status != ContributionStatus.committed:
        return HttpResponseForbidden()
    previous_data = {}
    related = list(Voyage.objects.filter(voyage_id__in=contribution.get_related_voyage_ids()))
    for voyage in related:
        dict = {}
        # Ship, nation, owners
        ship = voyage.voyage_ship
        if ship is not None:
            dict['name_of_vessel'] = ship.ship_name
            dict['year_ship_constructed'] = ship.year_of_construction
            dict['year_ship_registered'] = ship.registered_year
            dict['national_carrier'] = ship.nationality_ship_id
            dict['ship_construction_place'] = ship.vessel_construction_place_id
            dict['ship_registration_place'] = ship.registered_place_id
            dict['rig_of_vessel'] = ship.rig_of_vessel_id
            dict['tonnage_of_vessel'] = ship.tonnage
            dict['ton_type'] = ship.ton_type_id
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
        previous_data[voyage.voyage_id] = dict
    if request.method == 'POST':
        form = InterimVoyageForm(request.POST, instance=contribution.interim_voyage)
        prefix = 'interim_slave_number_'
        numbers = {k: int(v) for k, v in request.POST.items() if k.startswith(prefix) and v != ''}
        if form.is_valid():
            with transaction.atomic():
                form.save()
                # Clear previous numbers and save new ones.
                InterimSlaveNumber.objects.filter(interim_voyage__id=contribution.interim_voyage.pk).delete()
                for k, v in numbers.items():
                    number = InterimSlaveNumber()
                    number.interim_voyage = contribution.interim_voyage
                    number.var_name = k[len(prefix):]
                    number.number = v
                    number.save()
            return HttpResponseRedirect(reverse('contribute:thanks'))
    else:
        form = InterimVoyageForm(instance=contribution.interim_voyage)
        numbers = {n.var_name: n.number for n in contribution.interim_voyage.slave_numbers.all()}
    import json
    return render(request, 'contribute/interim.html',
                  {'form': form, 'numbers': numbers,
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

def under_construction(request):
    return JsonResponse({'error': 'UNDER CONSTRUCTION'})
