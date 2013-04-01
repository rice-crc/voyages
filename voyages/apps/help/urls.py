from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from voyages.apps.voyage.views import *

urlpatterns = patterns('django.views.generic.simple',
    url(r'^sitemap.html$', 'direct_to_template', {'template': 'help/sitemap.html'}),
    url(r'^faqs.html$', 'direct_to_template', {'template': 'help/faqs.html'}),
    url(r'^demos.html$', 'direct_to_template', {'template': 'help/demos.html'}),
    url(r'^glossary.html$', 'direct_to_template', {'template': 'help/glossary.html'}),
    url(r'^legal.html$', 'direct_to_template', {'template': 'help/legal.html'}),
)
