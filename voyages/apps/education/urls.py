from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# To be used later
# from voyages.apps.education.views import *

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'education/index.html'}),
    url(r'^index.html$', 'direct_to_template', {'template': 'education/index.html'}),
    url(r'^lesson-plans.html$', 'direct_to_template', {'template': 'education/lesson-plans.html'}),
    url(r'^others.html$', 'direct_to_template', {'template': 'education/others.html'}),
    #handle all cases for now
    url(r'^[\w\.\-]+\.html$', 'direct_to_template', {'template': 'education/index.html'}),
)
