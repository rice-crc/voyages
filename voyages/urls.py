from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from voyages.views import *
from voyages import sitemap

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#hide the Site and Group features
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group


# Sitemap
from django.contrib.sitemaps import Sitemap, FlatPageSitemap
from sitemap import StaticSitemap, ViewSitemap

urlpatterns = patterns('',
    # Homepage:
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}, name='index'),
    
    #Include url handlers of each section
    url(r'^voyage/', include('voyages.apps.voyage.urls', namespace='voyage')),
    url(r'^assessment/', include('voyages.apps.assessment.urls', namespace='assessment')),
    url(r'^about/', include('voyages.apps.about.urls', namespace='about')),
    url(r'^education/', include('voyages.apps.education.urls', namespace='education')),
    url(r'^resources/', include('voyages.apps.resources.urls', namespace='resources')),
    url(r'^help/', include('voyages.apps.help.urls', namespace='help')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^contribute/', include('voyages.apps.contribute.urls', namespace='contribute')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)

sitemaps = {
    'staticpages' : StaticSitemap(urlpatterns),
}

urlpatterns += patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name='sitemap-xml'),
      url('^pages/', include('django.contrib.flatpages.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
