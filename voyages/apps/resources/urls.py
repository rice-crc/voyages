from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView

import voyages.apps.resources.views
import voyages.apps.static_content.views

urlpatterns = [
    url(r'^$',
        voyages.apps.static_content.views.get_static_content,
        {'group': 'Resources'},
        name='index'),
    url(r'^about',
        TemplateView.as_view(template_name='resources/about.html'),
        name='about'),
    url(r'^downloads',
        TemplateView.as_view(template_name='resources/downloads.html'),
        name='downloads'),
    url(r'^lessons',
        TemplateView.as_view(template_name='resources/lessons.html'),
        name='lessons'),
    url(r'^links',
        TemplateView.as_view(template_name='resources/links.html'),
        name='links'),

    # handle all cases for now
    url(r'^images/category/(?P<category>\w+)/(?P<page>\d{1,3})/detail',
        voyages.apps.resources.views.get_image_detail,
        name='image-detail'),
    url(r'^images/category/(?P<category>\w+)/(?P<page>\d{1,3})',
        voyages.apps.resources.views.get_images_category_detail,
        name='images-category-detail'),
    url(r'^images/category/(?P<category>\w+)',
        voyages.apps.resources.views.get_images_category,
        name='images-category'),
    url(r'^images/search/(?P<page>\d{1,3})/detail',
        voyages.apps.resources.views.get_image_search_detail,
        name='image-search-detail-window'),
    url(r'^images/search/(?P<page>\d{1,3})',
        voyages.apps.resources.views.images_search_detail,
        name='images-search-detail'),
    url(r'^images/search',
        voyages.apps.resources.views.images_search,
        name='images-search'),
    url(r'^images/', voyages.apps.resources.views.get_all_images,
        name='images'),
    url(r'^names-database',
        voyages.apps.resources.views.get_all_slaves,
        name='origins')
]
