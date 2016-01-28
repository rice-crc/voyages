from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from voyages.apps.contribute import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^guidelines$', TemplateView.as_view(template_name='contribute/guidelines.html'), name='guidelines'),

    url(r'^thanks', TemplateView.as_view(template_name='contribute/thanks.html'), name='thanks'),

    url(r'^delete_voyage$', views.delete, name='delete_voyage'),

    url(r'^places_ajax$', views.get_places, name='places_ajax'),

    url(r'^voyage_ajax$', views.get_voyage_by_id, name='voyage_ajax'),

    url(r'interim/(?P<contribution_type>\w+)/(?P<contribution_id>\d+)$',
        views.interim, name='interim'),

    url(r'interim_summary/(?P<contribution_type>\w+)/(?P<contribution_id>\d+)$',
        views.interim_summary, name='interim_summary'),

    url(r'edit_voyage$', views.edit, name='edit_voyage'),

    url(r'merge_voyages$', views.merge, name='merge_voyages'),

    url(r'new_voyage$', views.new_voyage, name='new_voyage'),
)
