from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from voyages.apps.contribute.forms import LoginForm

urlpatterns = patterns('',
    url(r'^$', 'voyages.apps.contribute.views.index', name='index'),

    url(r'^guidelines$', TemplateView.as_view(template_name='contribute/guidelines.html'), name='guidelines'),
)
