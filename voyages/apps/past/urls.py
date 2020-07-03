from django.conf.urls import url
from django.views.generic import TemplateView

import voyages.apps.static_content.views
import voyages.apps.past.search_views
import voyages.apps.past.views

urlpatterns = [
    # url(r'^api/search', voyages.apps.past.search_views.ajax_search, name='search'),
    url(r'^api/search', voyages.apps.past.views.search_enslaved, name='search'),
    url(r'^api/modern-countries', voyages.apps.past.views.get_modern_countries, name='modern-countries'),
    url(r'^api/language-groups', voyages.apps.past.views.get_language_groups, name='language-groups'),
    url(r'^api/ethnicities', voyages.apps.past.views.get_ethnicities, name='ethnicities'),
    url(r'^database', TemplateView.as_view(template_name='past/database.html'), name='database')
    ]
