from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# To be used later
# from voyages.apps.resources.views import *

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'resources/index.html'}, name='index'),
    #handle all cases for now
    url(r'^images$', 'direct_to_template', {'template': 'under_constr.html'}, name='images'),
    url(r'^names-database', 'direct_to_template', {'template': 'under_constr.html'}, name='origins'),
    
    url(r'^images-detail$', 'direct_to_template', {'template': 'under_constr.html'}, name='images-detail'),
    url(r'^[\w\.\-]+\$', 'direct_to_template', {'template': 'under_constr.html'}),
)
