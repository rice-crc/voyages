from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from voyages.apps.assessment.views import *

urlpatterns = patterns('',
    url(r'^$', assessment_index, name='assessment_index'),
    url(r'^index.html$', assessment_index),
    
    #handle all cases for now
    url(r'^[\w\.\-]+\.html$', assessment_index),
)
