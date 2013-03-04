from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^help/index.html', 'voyages.apps.help.views.default', name='helpdefault'),
)
