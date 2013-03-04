from django.conf import settings
from django.conf.urls import patterns, include, url

from voyages.apps.resources import views

urlpatterns = patterns('',
    url(r'^$', 'voyages.apps.resources.views.resourceshome', name='resourceshome1'),
    url(r'^index.html$', 'voyages.apps.resources.views.resourceshome', name='resourceshome2'),
    
    #handle all cases for now
    url(r'^[\w\.\-]+\.html$', 'voyages.apps.resources.views.resourceshome', name='resourcehome3'),
)

