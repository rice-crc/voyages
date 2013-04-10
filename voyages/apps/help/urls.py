from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from voyages.apps.voyage.views import *

urlpatterns = patterns('django.views.generic.simple',
    url(r'^page_sitemap$', 'direct_to_template', {'template': 'help/page_sitemap.html'}),
    url(r'^page_faqs$', 'direct_to_template', {'template': 'help/page_faqs.html'}),
    url(r'^page_demos$', 'direct_to_template', {'template': 'help/page_demos.html'}),
    url(r'^page_glossary$', 'direct_to_template', {'template': 'help/page_glossary.html'}),
    url(r'^page_legal$', 'direct_to_template', {'template': 'help/page_legal.html'}),
    url(r'^page_demo-overview$', 'direct_to_template', {'template': 'help/page_demo-overview.html'}),
    url(r'^page_demo-search$', 'direct_to_template', {'template': 'help/page_demo-search.html'}),
    
    url(r'^help$', 'direct_to_template', {'template': 'help/helpbase.html'}, name='help'),
)
