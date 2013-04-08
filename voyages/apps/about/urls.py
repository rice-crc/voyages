from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# To be used later:
# from voyages.apps.about.views import *

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'about/index.html'}),
    url(r'^index.html$', 'direct_to_template', {'template': 'about/index.html'}, name='index'),
    url(r'^history.html$', 'direct_to_template', {'template': 'about/history.html'}, name='history'),
    url(r'^team.html$', 'direct_to_template', {'template': 'about/team.html'}, name='team'),
    url(r'^data.html$', 'direct_to_template', {'template': 'about/data.html'}, name='data'),
    url(r'^acknowledgements.html$', 'direct_to_template', {'template': 'about/acknowledgements.html'}, name='acknowledgements'),
    url(r'^origins.html$', 'direct_to_template', {'template': 'about/origins.html'}, name='origins'),
    url(r'^contacts.html$', 'direct_to_template', {'template': 'about/contacts.html'}, name='contacts'),
    
)

