from django.conf.urls import *
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('',
    url(r'^c(?P<chapternum>\w{2})_s(?P<sectionnum>\w{2})_p(?P<pagenum>\w{2})$',
        'voyages.apps.voyage.views.get_page', name='get-page'),
    url(r'^source/(?P<category>\w+)/(?P<sort>\w+)$',
        'voyages.apps.voyage.views.sources_list', name='sources-list-sort'),
    url(r'^source/(?P<category>\w+)$',
        'voyages.apps.voyage.views.sources_list', name='sources-list'),
    url(r'^source$',
        'voyages.apps.voyage.views.sources_list', name='sources-list-default')
)

urlpatterns += patterns('',
    url(r'^$', 'voyages.apps.static_content.views.get_static_content', {'group': 'Voyage'}, name='index'),
    url(r'^understanding-db$', TemplateView.as_view(template_name='voyage/understanding_base.html'), name='guide'),
    url(r'^understanding-db/(?P<name>.*)', 'voyages.apps.voyage.views.understanding_page' , name='understanding-page'),

    url(r'^c01_s01_cover$', TemplateView.as_view(template_name='voyage/guide.html'), name='voyage-guide-intro'),
    #url(r'^c01_s03_cover$', 'voyages.apps.voyage.views.variable_list', name='variables'),
    url(r'^search', 'voyages.apps.voyage.views.search', name='search'),

    url(r'^contribute$', RedirectView.as_view(url='/contribute'), name='submission-login'),
    
    url(r'^voyage$', TemplateView.as_view(template_name='under_constr.html'), name='voyage'),
    url(r'^(?P<voyage_id>[0-9]+)/variables$', 'voyages.apps.voyage.views.voyage_variables', name='voyage_variables'),
    url(r'^(?P<voyage_id>[0-9]+)/map$', 'voyages.apps.voyage.views.voyage_map', name='voyage_map'),
    url(r'^(?P<voyage_id>[0-9]+)/images$', 'voyages.apps.voyage.views.voyage_images', name='voyage_images'),

    url(r'^csv_stats_download', 'voyages.apps.voyage.views.csv_stats_download', name='csv_stats_download'),
    url(r'^shorten_search_url', 'voyages.apps.voyage.views.shorten_search_url', name='shorten_search_url'),
)

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^download$', 'flatpage', {'url': '/voyage/download/'}, name='download'),
)
