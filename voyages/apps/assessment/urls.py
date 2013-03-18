from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('',
     url(r'^essay-(?P<pagenum>\d{2}).html$','voyages.apps.assessment.views.getessay'),                
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'assessment/index.html'}),
    url(r'^index.html$', 'direct_to_template', {'template': 'assessment/index.html'}),
)
