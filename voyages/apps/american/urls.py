from django.conf.urls import url
from django.views.generic import TemplateView
import voyages.apps.american.views

import voyages.apps.static_content.views

urlpatterns = [
    # url(r'^$', voyages.apps.static_content.views.get_static_content, {'group': 'About'}, name='index'),
    # url(r'^$', TemplateView.as_view(template_name='american/about.html'), name='about'),
    url(r'^about', TemplateView.as_view(template_name='american/about.html'), name='about'),
    url(r'^essays', TemplateView.as_view(template_name='american/essays.html'), name='essays'),
    url(r'^downloads', TemplateView.as_view(template_name='american/downloads.html'), name='downloads'),
    url(r'^database', voyages.apps.american.views.index, name='database'), # url(r'^database', TemplateView.as_view(template_name='american/database.html'), name='database'),
    url(r'^api/beta_ajax_search', voyages.apps.voyage.beta_views.ajax_search, name='beta_ajax_search'),
    url(r'^api/beta_ajax_download', voyages.apps.voyage.beta_views.ajax_download, name='beta_ajax_download'),
    url(r'^api', voyages.apps.voyage.beta_views.search_view, name='beta_search')
]