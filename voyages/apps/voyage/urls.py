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
    url(r'^$', TemplateView.as_view(template_name='voyage/index.html'), name='index'),
    url(r'^understanding-db$', TemplateView.as_view(template_name='voyage/c01_base.html'), name='guide'),

    url(r'^c01_s01_cover$', TemplateView.as_view(template_name='voyage/c01_s01_cover.html'), name='voyage-guide-intro'),
    url(r'^c01_s03_cover$', 'voyages.apps.voyage.views.variable_list', name='variables'),
    url(r'^search', 'voyages.apps.voyage.views.search', name='search'),

    url(r'^contribute$', RedirectView.as_view(url='/contribute'), name='submission-login'),
    
    url(r'^voyage$', TemplateView.as_view(template_name='under_constr.html'), name='voyage'),

    url(r'^csv_all_download/(-?\d+)/$', 'voyages.apps.voyage.views.download_results', name='csv_all_download'),
    url(r'^csv_stats_download', 'voyages.apps.voyage.views.csv_stats_download', name='csv_stats_download'),
)

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^download$', 'flatpage', {'url': '/voyage/download/'}, name='download'),
)
