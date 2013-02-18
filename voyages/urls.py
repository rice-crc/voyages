from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'voyages.views.home', name='home'),
    # url(r'^voyages/', include('voyages.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': 'static'}  ),
    #url(r'^static/(.*)$','django.views.static.serve',{'document_root': 'static'}  ),

    # url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
	# url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
