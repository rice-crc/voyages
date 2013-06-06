from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from voyages.apps.voyage.views import *
from voyages.apps.help import views

urlpatterns = patterns('django.views.generic.simple',
    url(r'^page_sitemap$', 'direct_to_template', {'template': 'help/page_sitemap.html'}, name='sitemap'),
    #url(r'^page_faqs$', 'direct_to_template', {'template': 'help/page_faqs.html'}, name='faqs'),
    url(r'^page_demos$', 'direct_to_template', {'template': 'help/page_demos.html'}, name='demos'),
    #url(r'^page_glossary$', 'direct_to_template', {'template': 'help/page_glossary.html'}, name='glossary'),
    url(r'^page_legal$', 'direct_to_template', {'template': 'help/page_legal.html'}, name='legal'),
    url(r'^page_demo-overview$', 'direct_to_template', {'template': 'help/page_demo-overview.html'}, name='demo-overview'),
    url(r'^page_demo-search$', 'direct_to_template', {'template': 'help/page_demo-search.html'}, name='demo-search'),
    
    url(r'^help$', 'direct_to_template', {'template': 'help/helpbase.html'}, name='help'),
)

urlpatterns += patterns('',
    url(r'^page_glossary$', 'voyages.apps.help.views.glossaryPage', name='glossary'),
    url(r'^page_faqs', 'voyages.apps.help.views.get_faqs', name='faqs'),
)
