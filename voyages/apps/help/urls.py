from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from voyages.apps.voyage.views import *

urlpatterns = patterns('django.views.generic.simple',
    url(r'^page_sitemap.html$', 'direct_to_template', {'template': 'help/page_sitemap.html'}),
    url(r'^page_faqs.html$', 'direct_to_template', {'template': 'help/page_faqs.html'}),
    url(r'^page_demos.html$', 'direct_to_template', {'template': 'help/page_demos.html'}),
    url(r'^page_glossary.html$', 'direct_to_template', {'template': 'help/page_glossary.html'}),
    url(r'^page_legal.html$', 'direct_to_template', {'template': 'help/page_legal.html'}),
    url(r'^page_demo-overview.html$', 'direct_to_template', {'template': 'help/page_demo-overview.html'}),
    url(r'^page_demo-search.html$', 'direct_to_template', {'template': 'help/page_demo-search.html'}),
    
    url(r'^help.html$', 'direct_to_template', {'template': 'help/helpbase.html'}, name='help'),
)
