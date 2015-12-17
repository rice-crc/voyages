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
from voyages.apps.voyage.models import Voyage

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
    error = None
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

@login_required
def delete(request):
    voyage_selection = []
    if request.method == 'POST':
        form = DeleteContributionForm(request.POST)
        if form.is_valid():
            ids = form.cleaned_data['delete_ids']
            with transaction.atomic():
                note = ContributionNote()
                note.tag = 'DeleteContributionForm'
                note.note = form.cleaned_data['notes']
                note.save()
                contribution = DeleteVoyageContribution()
                contribution.contributor = request.user
                contribution.deleted_voyages_ids = ','.join([str(x) for x in ids])
                contribution.status = ContributionStatus.committed
                contribution.save()
                contribution.notes.add(note)
                contribution.save()
            return HttpResponseRedirect(reverse('contribute:thanks'))
        else:
            ids = form.cleaned_data.get('delete_ids', [])
            voyage_selection = [get_summary(v) for v in Voyage.objects.filter(voyage_id__in=ids)]
    else:
        form = DeleteContributionForm()
    return render(request, 'contribute/delete.html', {'form': form, 'voyage_selection': voyage_selection})

contribution_model_by_type = {
    'edit': EditVoyageContribution,
    'merge': MergeVoyagesContribution,
    'new': NewVoyageContribution
}

@login_required
def interim(request, contribution_type, contribution_id):
    notes = ''
    model = contribution_model_by_type.get(contribution_type)
    if model is None:
        raise Http404
    contribution = model.objects.get(pk=contribution_id)
    if contribution.status != ContributionStatus.pending:
        return HttpResponseForbidden()
    if request.method == 'POST':
        notes = request.POST.get('all_notes', '')
        form = InterimVoyageForm(request.POST, instance=contribution.interim_voyage)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('contribute:thanks'))
    else:
        form = InterimVoyageForm(instance=contribution.interim_voyage)
    return render(request, 'contribute/interim.html',
                  {'form': form, 'notes': notes})

@login_required
def new_voyage_contribution(request):
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
