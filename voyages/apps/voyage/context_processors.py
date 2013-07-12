from .models import *
from django.db.models import Max, Min

def voyage_span(request):
    """
    Obtain the first and last year when voyages began
    """
    return {
       'voyage_span_first_year': VoyageDates.objects.all().aggregate(Min('imp_voyage_began'))['imp_voyage_began__min'][2:],
       'voyage_span_last_year' : VoyageDates.objects.all().aggregate(Max('imp_voyage_began'))['imp_voyage_began__max'][2:],
    }