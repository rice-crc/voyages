from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# To be used later
# from voyages.apps.resources.views import *

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'resources/index.html'}),
    url(r'^index.html$', 'direct_to_template', {'template': 'resources/index.html'}),
    #handle all cases for now
    url(r'^images.html$', 'direct_to_template', {'template': 'under_constr.html'}),
    url(r'^origins.html$', 'direct_to_template', {'template': 'under_constr.html'}),
    
    url(r'^[\w\.\-]+\.html$', 'direct_to_template', {'template': 'under_constr.html'}),
)
