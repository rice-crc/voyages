from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from voyages.apps.voyage.views import *

urlpatterns = patterns('',
    url(r'^$', voyage_index, name='voyage_index'),
    url(r'^index.html$', voyage_index),
    
    #handle all cases for now
    url(r'^[\w\.\-]+\.html$', voyage_index),
)

