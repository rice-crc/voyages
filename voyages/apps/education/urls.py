from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from voyages.apps.education import views

urlpatterns = patterns('',
    url(r'^$', 'voyages.apps.education.views.educationhome', name='educationhome1'),
    url(r'^index.html$', 'voyages.apps.education.views.educationhome', name='educationhome2'),
    
    #handle all cases for now
    url(r'^[\w\.\-]+\.html$', 'voyages.apps.education.views.educationhome', name='educationhome3'),
)

