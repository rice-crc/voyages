from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.sitemaps import Sitemap, FlatPageSitemap
sitemaps = {
  'site': Sitemap,
  'flatpages': FlatPageSitemap,
}

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'voyages.views.myhome', name='myhome'),
    url(r'^index.html$', 'voyages.views.myhome', name='myhome'),
    url(r'^defhome.html$', 'voyages.views.defhome', name='defhome'),
    
    # database = voyage
    url(r'^database/', include('voyages.apps.voyage.urls', namespace='voyages.apps.voyage')),
    url(r'^assessment/', include('voyages.apps.assessment.urls', namespace='voyages.apps.assessment')),
    url(r'^about/', include('voyages.apps.about.urls', namespace='voyages.apps.about')),
    url(r'^education/', include('voyages.apps.education.urls', namespace='voyages.apps.education')),
    url(r'^resources/', include('voyages.apps.resources.urls', namespace='voyages.apps.resources')),
    
    # url(r'^voyages/', include('voyages.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    

    #url(r'^help/', include('voyages.apps.database', namespace='database')),
    
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/path/to/media'}),
    
    #url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': 'static'}  ),
    #url(r'^static/(.*)$','django.views.static.serve',{'document_root': 'static'}  ),

    # url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
	 url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
