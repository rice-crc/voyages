from __future__ import absolute_import, unicode_literals

import django.contrib.sitemaps.views
import django.views.i18n
import django.views.static
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

# Comment out the two autocomplete lines to disable the admin:
from autocomplete_light import shortcuts as autocomplete_light
import voyages.apps.assessment.views
import voyages.apps.common.views
import voyages.apps.past.views
import voyages.apps.voyage.views

from .sitemap import StaticSitemap

autocomplete_light.autodiscover()

admin.autodiscover()

# Sitemap

js_info_dict = {
    'packages': ('voyages',),
}

urlpatterns = [
    url(r'^',
        include('voyages.apps.static_content.urls',
                namespace='static_content')),
    # Short permalink
    url(r'^estimates/(?P<link_id>\w+)',
        voyages.apps.assessment.views.restore_permalink,
        name='restore_e_permalink'),
    url(r'^voyages/(?P<link_id>\w+)',
        voyages.apps.voyage.views.restore_permalink,
        name='restore_v_permalink'),
    url(r'^past-db/(?P<link_id>\w+)',
        voyages.apps.past.views.restore_permalink,
        name='restore_past_permalink'),

    # Include url handlers of each section
    url(r'^voyage/', include('voyages.apps.voyage.urls', namespace='voyage')),
    url(r'^american/',
        include('voyages.apps.american.urls', namespace='american')),
    url(r'^assessment/',
        include('voyages.apps.assessment.urls', namespace='assessment')),
    url(r'^about/', include('voyages.apps.about.urls', namespace='about')),
    url(r'^common/', include('voyages.apps.common.urls', namespace='common')),
    url(r'^past/', include('voyages.apps.past.urls', namespace='past')),
    url(r'^resources/',
        include('voyages.apps.resources.urls', namespace='resources')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^contribute/',
        include('voyages.apps.contribute.urls', namespace='contribute')),
    url(r'^search/', include('haystack.urls', namespace='search')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    # Handle language changes
    url(r'^setlanguage/(?P<lang_code>\w+)',
        voyages.apps.common.views.set_language,
        name='set_lang'),

    # Translation support for javascript code.
    url(r'^jsi18n/',
        django.views.i18n.javascript_catalog,
        js_info_dict,
        name='javascript-catalog'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^captcha/', include('captcha.urls'))
]

# XML generated sitemap
sitemaps = {
    'staticpages': StaticSitemap(urlpatterns),
}
# URLs not included in the sitemap
urlpatterns += [
    url(r'^sitemap\.xml',
        django.contrib.sitemaps.views.sitemap, {'sitemaps': sitemaps},
        name='sitemap-xml'),

    # Flatpages
    url(r'^pages/', include('django.contrib.flatpages.urls')),

    # Adding download files
    url(r'^admin/downloads',
        voyages.apps.voyage.views.download_file,
        name="downloads"),

    # Admin documentation
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin management
    url(r'^admin/', include(admin.site.urls))
]

# Serving static files including files uploaded by users
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^documents/(?P<path>.*)', django.views.static.serve,
            {'document_root': settings.MEDIA_ROOT})
    ]
