from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('',
     url(r'^essays-intro-(?P<pagenum>\d{2}).html$','voyages.apps.assessment.views.get_intro'),
     url(r'^essays-seasonality-(?P<pagenum>\d{2}).html$','voyages.apps.assessment.views.get_seasonality'),  
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'assessment/index.html'}),
    url(r'^index.html$', 'direct_to_template', {'template': 'assessment/index.html'}, name='index'),
    url(r'^essays.html$', 'direct_to_template', {'template': 'assessment/essaybase.html'}, name='essays'),
    
    url(r'^essays-grandio.html$', 'direct_to_template', {'template': 'assessment/essays-grandio.html'}, name='essays-grandio'),
    url(r'^essays-solomon.html$', 'direct_to_template', {'template': 'assessment/essays-solomon.html'}, name='essays-solomon'),
    url(r'^essays-mulgrave.html$', 'direct_to_template', {'template': 'assessment/essays-mulgrave.html'}, name='essays-mulgrave'),
    url(r'^essays-applied-history.html$', 'direct_to_template', {'template': 'assessment/essays-applied-history.html'}, name='essays-applied-history'),
    
    url(r'intro-maps.html$', 'direct_to_template', {'template': 'assessment/intro-maps.html'}, name='intro-maps'),
    url(r'^estimates.html$', 'direct_to_template', {'template': 'under_constr.html'}, name='estimates'),
)
