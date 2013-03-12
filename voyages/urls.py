from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from voyages.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.sitemaps import Sitemap, FlatPageSitemap
sitemaps = {
  'site': Sitemap,
  'flatpages': FlatPageSitemap,
}

urlpatterns = patterns('',
    # Homepage:
    url(r'^$', index, name='index'),
    url(r'^index.html$', index),
    url(r'^defhome.html$', index),
    
    #Each section handler 
    url(r'^database/', include('voyages.apps.voyage.urls', namespace='voyages.apps.voyage')),
    url(r'^assessment/', include('voyages.apps.assessment.urls', namespace='voyages.apps.assessment')),
    url(r'^about/', include('voyages.apps.about.urls', namespace='voyages.apps.about')),
    url(r'^education/', include('voyages.apps.education.urls', namespace='voyages.apps.education')),
    url(r'^resources/', include('voyages.apps.resources.urls', namespace='voyages.apps.resources')),
    
    #url(r'^help/', include('voyages.apps.database', namespace='database')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    

    # url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
	 url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
