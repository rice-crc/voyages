from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView

import voyages.apps.american.views

urlpatterns = [
    url(r'^about',
        TemplateView.as_view(template_name='american/about.html'),
        name='about'),
    url(r'^essays',
        TemplateView.as_view(template_name='american/essays.html'),
        name='essays'),
    url(r'^downloads',
        TemplateView.as_view(template_name='american/downloads.html'),
        name='downloads'),
    # url(r'^database',
    # TemplateView.as_view(template_name='american/database.html'),
    # name='database'),
    url(r'^database', voyages.apps.american.views.index, name='database'),
    url(r'^api/search',
        voyages.apps.voyage.search_views.ajax_search,
        name='search'),
    url(r'^api/download',
        voyages.apps.voyage.search_views.ajax_download,
        name='download'),
]
