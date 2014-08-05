from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^$', 'voyages.apps.static_content.views.get_static_content', name='index'),
)