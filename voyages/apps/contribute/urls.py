from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from voyages.apps.contribute.forms import LoginForm

urlpatterns = patterns('',
    url(r'^$', 'voyages.apps.contribute.views.index', name='index'),

    url(r'^guidelines$', TemplateView.as_view(template_name='contribute/guidelines.html'), name='guidelines'),

    url(r'^thanks', TemplateView.as_view(template_name='contribute/thanks.html'), name='thanks'),

    url(r'^delete$', 'voyages.apps.contribute.views.delete', name='delete'),

    url(r'^voyage_ajax', 'voyages.apps.contribute.views.get_voyage_by_id', name='voyage_ajax'),
)
