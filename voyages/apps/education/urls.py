from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# To be used later
# from voyages.apps.education.views import *

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'education/index.html'}),
    url(r'^index.html$', 'direct_to_template', {'template': 'education/index.html'}, name='index'),
    url(r'^lesson-plans.html$', 'direct_to_template', {'template': 'education/lesson-plans.html'}, name='lesson-plans'),
    url(r'^others.html$', 'direct_to_template', {'template': 'education/others.html'}, name='others'),
    #handle all cases for now
    url(r'^[\w\.\-]+\.html$', 'direct_to_template', {'template': 'under_constr.html'}),
)
