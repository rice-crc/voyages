from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('',
     url(r'^methodology-(?P<pagenum>\d{2}).html$','voyages.apps.voyage.views.getmethodology'),                
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'voyage/index.html'}),
    url(r'^index.html$', 'direct_to_template', {'template': 'voyage/index.html'}),
    url(r'^guide.html$', 'direct_to_template', {'template': 'voyage/guide.html'}),  
    url(r'^tmpcheck.html$', 'direct_to_template', {'template': 'voyage/page_01.html'}),  
)
