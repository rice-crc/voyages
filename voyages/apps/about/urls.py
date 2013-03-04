from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from voyages.apps.about import views

urlpatterns = patterns('',
    url(r'^$', 'voyages.apps.about.views.abouthome', name='abouthome1'),
    url(r'^index.html$', 'voyages.apps.about.views.abouthome', name='abouthome2'),
    
    #handle all cases for now
    url(r'^[\w\.\-]+\.html$', 'voyages.apps.about.views.abouthome', name='abouthome3'),
)

