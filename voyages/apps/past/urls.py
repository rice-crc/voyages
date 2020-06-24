from django.conf.urls import url
from django.views.generic import TemplateView

import voyages.apps.static_content.views
import voyages.apps.past.search_views
import voyages.apps.past.views

urlpatterns = [
    url(r'^$', voyages.apps.static_content.views.get_static_content, {'group': 'Past'},
        name='index'),

    #handle all cases for now
    # url(r'^api/search', voyages.apps.past.views.search_enslaved, name='search'),
    url(r'^api/search', voyages.apps.past.search_views.ajax_search, name='search'),
    url(r'^database', TemplateView.as_view(template_name='past/database.html'), name='database')
    ]
