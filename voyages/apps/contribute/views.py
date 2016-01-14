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

number_prefix = 'interim_slave_number_'

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
                init_interim_voyage(interim_voyage, contribution)
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
    previous_data = contribution_related_data(contribution)
    sources_post = None
    if request.method == 'POST':
        if request.POST.get('submit_val') == 'delete':
            with transaction.atomic():
                contribution.interim_voyage.delete()
                contribution.delete()
            return HttpResponseRedirect(reverse('contribute:index'))
        else:
            form = InterimVoyageForm(request.POST, instance=contribution.interim_voyage)
            prefix = 'interim_slave_number_'
            numbers = {k: int(v) for k, v in request.POST.items() if k.startswith(prefix) and v != ''}
            import json
            sources_post = request.POST.get('sources')
            sources = [create_source(x, contribution.interim_voyage)
                       for x in json.loads(sources_post if sources_post is not None else '[]')]
            if form.is_valid():
                with transaction.atomic():
                    def del_children(child_model):
                        child_model.objects.filter(interim_voyage__id=contribution.interim_voyage.pk).delete()
                    del_children(InterimPrimarySource)
                    del_children(InterimArticleSource)
                    del_children(InterimBookSource)
                    del_children(InterimOtherSource)
                    del_children(InterimSlaveNumber)
                    form.save()
                    for src in sources:
                        src.save()
                    # Clear previous numbers and save new ones.
                    for k, v in numbers.items():
                        number = InterimSlaveNumber()
                        number.interim_voyage = contribution.interim_voyage
                        number.var_name = k[len(prefix):]
                        number.number = v
                        number.save()
                return HttpResponseRedirect(reverse('contribute:thanks'))
    else:
        numbers = {number_prefix + n.var_name: n.number for n in contribution.interim_voyage.slave_numbers.all()}
        form = InterimVoyageForm(instance=contribution.interim_voyage)
    import json
    return render(request, 'contribute/interim.html',
                  {'form': form,
                   'numbers': numbers,
                   'interim': contribution.interim_voyage,
                   'sources_post': sources_post,
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

def contribution_related_data(contribution):    
    previous_data = {}
    related = contribution.get_related_voyages()
    for voyage in related:
        previous_data[voyage.voyage_id] = voyage_to_dict(voyage)
    return previous_data

def voyage_to_dict(voyage):
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
