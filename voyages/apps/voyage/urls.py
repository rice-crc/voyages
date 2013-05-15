from django.conf import settings
from django.conf.urls.defaults import *
from voyages.apps.voyage.views import *


urlpatterns = patterns('',
    url(r'^c(?P<chapternum>\d{2})_s(?P<sectionnum>\d{2})_p(?P<pagenum>\d{2})$','voyages.apps.voyage.views.get_page', name='get-page'),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'voyage/index.html'}, name='index'),
    url(r'^understanding-db$', 'direct_to_template', {'template': 'voyage/c01_base.html'}, name='guide'),
    
    url(r'^c01_s01_cover$', 'direct_to_template', {'template': 'voyage/c01_s01_cover.html'}, name='voyage-guide-intro'),
    url(r'^c01_s03_cover$', 'direct_to_template', {'template': 'raw_under_constr.html'}, name='variables'), 
    url(r'^c01_s04_cover$', 'direct_to_template', {'template': 'raw_under_constr.html'}, name='sources'), 
    
    url(r'^search$', 'direct_to_template', {'template': 'under_constr.html'}, name='search'),

    url(r'^contribute$', 'redirect_to', {'url':'/contribute'}, name='submission-login'),
    
    #url(r'^c04_s01_cover$', 'direct_to_template', {'template': 'voyage/c04_s01_cover.html'}, name='contrib-guidelines'),
    #url(r'^c04_s02_cover$',  'redirect_to', {'url':'/contribute'}, name='sign-in'),
   
    url(r'^voyage$', 'direct_to_template', {'template': 'under_constr.html'}, name='voyage'),
)

urlpatterns += patterns('django.contrib.flatpages.views',
        url(r'^download$', 'flatpage', {'url': '/voyage/download/'}, name='download'),
)
