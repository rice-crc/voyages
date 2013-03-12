from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from voyages.apps.resources.views import *

urlpatterns = patterns('',
    url(r'^$', resources_index, name='resources_index'),
    url(r'^index.html$', resources_index),
    
    #handle all cases for now
    url(r'^[\w\.\-]+\.html$', resources_index),
)

