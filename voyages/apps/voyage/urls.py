from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView

import voyages.apps.voyage.views
import voyages.apps.voyage.beta_views
import voyages.apps.static_content.views

urlpatterns = [

    # flatpages
    url(r'^about', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^essays', TemplateView.as_view(template_name='essays.html'), name='essays'),
    url(r'^downloads', TemplateView.as_view(template_name='downloads.html'), name='downloads'),
    url(r'^maps', TemplateView.as_view(template_name='maps.html'), name='maps'),


    url(r'^c(?P<chapternum>\w{2})_s(?P<sectionnum>\w{2})_p(?P<pagenum>\w{2})',
        voyages.apps.voyage.views.get_page, name='get-page'),
    url(r'^source/(?P<category>\w+)/(?P<sort>\w+)',
        voyages.apps.voyage.views.sources_list, name='sources-list-sort'),
    url(r'^source/(?P<category>\w+)',
        voyages.apps.voyage.views.sources_list, name='sources-list'),
    url(r'^source',
        voyages.apps.voyage.views.sources_list, name='sources-list-default'),
    url(r'^$', voyages.apps.static_content.views.get_static_content, {'group': 'Voyage'}, name='index'),
    url(r'^understanding-db/(?P<name>.*)', voyages.apps.voyage.views.understanding_page, name='understanding-page'),
    url(r'^understanding-db', voyages.apps.voyage.views.understanding_page, name='guide'),

    url(r'^c01_s01_cover', TemplateView.as_view(template_name='guide.html'), name='voyage-guide-intro'),
    #url(r'^c01_s03_cover', voyages.apps.voyage.views.variable_list, name='variables'),
    url(r'^reload-cache', voyages.apps.voyage.views.reload_cache, name='reload_cache'),

    url(r'^search', voyages.apps.voyage.views.search, name='search'),

    url(r'^permalink', voyages.apps.voyage.views.get_permanent_link, name='permanent-link'),

    url(r'^contribute', RedirectView.as_view(url='/contribute'), name='submission-login'),

    url(r'^(?P<voyage_id>[0-9]+)/variables', voyages.apps.voyage.views.voyage_variables, name='voyage_variables'),
    url(r'^(?P<voyage_id>[0-9]+)/map', voyages.apps.voyage.views.voyage_map, name='voyage_map'),
    url(r'^(?P<voyage_id>[0-9]+)/images', voyages.apps.voyage.views.voyage_images, name='voyage_images'),

    url(r'^csv_stats_download', voyages.apps.voyage.views.csv_stats_download, name='csv_stats_download'),
    # url(r'^download', voyages.apps.voyage.views.download_flatpage, name='download'),
    url(r'^download', TemplateView.as_view(template_name='download.html'), name='download'),

    url(r'^database', TemplateView.as_view(template_name='database.html'), name='database'),


    url(r'var-options', voyages.apps.voyage.beta_views.get_var_options, name='var-options'),
    url(r'filtered-places', voyages.apps.voyage.beta_views.get_filtered_places, name='filtered-places'),
    url(r'save-query', voyages.apps.voyage.beta_views.save_query, name='save-query'),
    url(r'get-saved-query/(?P<query_id>\w+)', voyages.apps.voyage.beta_views.get_saved_query, name='get-saved-query'),

    url(r'^api/beta_ajax_search', voyages.apps.voyage.beta_views.ajax_search, name='beta_ajax_search'),
    url(r'^api/beta_ajax_download', voyages.apps.voyage.beta_views.ajax_download, name='beta_ajax_download'),
    url(r'^api', voyages.apps.voyage.beta_views.search_view, name='beta_search'),

    url(r'get-all-sources', voyages.apps.voyage.beta_views.get_all_sources, name='all-sources'),
]
