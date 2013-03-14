from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from voyages.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Sitemap
from django.contrib.sitemaps import Sitemap, FlatPageSitemap
sitemaps = {
  'site': Sitemap,
  'flatpages': FlatPageSitemap,
}

urlpatterns = patterns('',
    # Homepage:
    url(r'^$', index, name='index'),
    
    #Include url handlers of each section
    url(r'^voyage/', include('voyages.apps.voyage.urls', namespace='voyage')),
    url(r'^assessment/', include('voyages.apps.assessment.urls', namespace='assessment')),
    url(r'^about/', include('voyages.apps.about.urls', namespace='about')),
    url(r'^education/', include('voyages.apps.education.urls', namespace='education')),
    url(r'^resources/', include('voyages.apps.resources.urls', namespace='resources')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    
    # Sitemap/Help section
    #url(r'^help/', include('voyages.apps.database', namespace='database')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    

    # url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
	 url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
