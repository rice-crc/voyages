from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from voyages.apps.education.views import *

urlpatterns = patterns('',    
    url(r'^$', education_index, name='education_index'),
    url(r'^index.html$', education_index),
    
    #handle all cases for now
    url(r'^[\w\.\-]+\.html$', education_index),
)

