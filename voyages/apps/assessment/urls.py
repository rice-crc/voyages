from django.conf import settings
from django.conf.urls import patterns, include, url

from voyages.apps.assessment import views

urlpatterns = patterns('',
    url(r'^$', 'voyages.apps.assessment.views.asmthome', name='assessmenthome1'),
    url(r'^index.html$', 'voyages.apps.assessment.views.asmthome', name='assessmenthome2'),
    
    #handle all cases for now
    url(r'^[\w\.\-]+\.html$', 'voyages.apps.assessment.views.asmthome', name='assessmenthome3'),
)

