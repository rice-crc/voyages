from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^sitemap.html$', 'direct_to_template', {'template': 'help/sitemap.html'}),
    url(r'^faqs.html$', 'direct_to_template', {'template': 'help/faqs.html'}),
    url(r'^demos.html$', 'direct_to_template', {'template': 'help/demos.html'}),
    url(r'^glossary.html$', 'direct_to_template', {'template': 'help/glossary.html'}),
    url(r'^legal.html$', 'direct_to_template', {'template': 'help/legal.html'}),
)
