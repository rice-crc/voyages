from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# To be used later
# from voyages.apps.education.views import *

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'education/index.html'}, name='index'),
    url(r'^lesson-plans$', 'direct_to_template', {'template': 'education/lesson-plans.html'}, name='lesson-plans'),
    url(r'^web-resources$', 'direct_to_template', {'template': 'education/others.html'}, name='others'),
)
