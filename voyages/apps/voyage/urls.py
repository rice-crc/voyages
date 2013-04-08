from django.conf import settings
from django.conf.urls.defaults import *
from voyages.apps.voyage.views import *

urlpatterns = patterns('',
    url(r'^method-(?P<pagenum>\d{2}).html$','voyages.apps.voyage.views.get_methodology'),              
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'voyage/index.html'}),
    url(r'^index.html$', 'direct_to_template', {'template': 'voyage/index.html'}, name='index'),
    url(r'^guide.html$', 'direct_to_template', {'template': 'voyage/guide.html'}, name='guide'),
    url(r'^voyage-guide-intro.html$', 'direct_to_template', {'template': 'voyage/voyage-guide-intro.html'}, name='voyage-guide-intro'),
    
    url(r'^search.html$', 'direct_to_template', {'template': 'under_constr.html'}, name='search'),
    url(r'^download.html$', 'direct_to_template', {'template': 'under_constr.html'}, name='download'),
    url(r'^submission-login.html$', 'direct_to_template', {'template': 'under_constr.html'}, name='submission-login'),
    url(r'^variables.html$', 'direct_to_template', {'template': 'under_constr.html'}, name='variables'),
    url(r'^sources.html$', 'direct_to_template', {'template': 'under_constr.html'}, name='sources'),
    url(r'^voyage.html$', 'direct_to_template', {'template': 'under_constr.html'}, name='voyage'),
)
