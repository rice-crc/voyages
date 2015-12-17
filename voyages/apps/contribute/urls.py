from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'voyages.apps.contribute.views.index', name='index'),

    url(r'^guidelines$', TemplateView.as_view(template_name='contribute/guidelines.html'), name='guidelines'),

    url(r'^thanks', TemplateView.as_view(template_name='contribute/thanks.html'), name='thanks'),

    url(r'^delete_voyage$', 'voyages.apps.contribute.views.delete', name='delete_voyage'),

    url(r'^voyage_ajax$', 'voyages.apps.contribute.views.get_voyage_by_id', name='voyage_ajax'),

    url(r'interim/(?P<contribution_type>\w+)/(?P<contribution_id>\d+)$',
        'voyages.apps.contribute.views.interim', name='interim'),

    url(r'edit_voyage$', 'voyages.apps.contribute.views.under_construction', name='edit_voyage'),

    url(r'merge_voyage$', 'voyages.apps.contribute.views.under_construction', name='merge_voyage'),

    url(r'new_voyage$', 'voyages.apps.contribute.views.new_voyage_contribution', name='new_voyage'),
)
