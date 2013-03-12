from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from voyages.apps.about.views import *

urlpatterns = patterns('',
    url(r'^$', about_index, name='about_index'),
    url(r'^index.html$', about_index),
    
    #handle all cases for now
    url(r'^[\w\.\-]+\.html$', about_index),
)

