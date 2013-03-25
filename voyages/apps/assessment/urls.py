from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('',
     # url(r'^essays-intro-(?P<pagenum>\d{2}).html$','voyages.apps.assessment.views.getintro'),
     # url(r'^essays-seasonality-(?P<pagenum>\d{2}).html$','voyages.apps.assessment.views.getseasonality'),
     url(r'^essays-intro-(?P<pagenum>\d{2}).html$','voyages.apps.assessment.views.get_intro'),
     url(r'^essays-seasonality-(?P<pagenum>\d{2}).html$','voyages.apps.assessment.views.get_seasonality'),  
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'assessment/index.html'}),
    url(r'^index.html$', 'direct_to_template', {'template': 'assessment/index.html'}),
    url(r'^essays.html$', 'direct_to_template', {'template': 'assessment/essaybase.html'}),
)
