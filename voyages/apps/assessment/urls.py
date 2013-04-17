from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('',
     # for both sections 1 and 2  
     url(r'^c(?P<chapternum>\d{2})_s(?P<sectionnum>\d{2})_p(?P<pagenum>\d{2})$','voyages.apps.assessment.views.get_page', name='get-page'), 
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'assessment/index.html'}, name='index'),
    url(r'^essays$', 'direct_to_template', {'template': 'assessment/c01_base.html'}, name='essays'),
    
    url(r'^c01_s03_cover$', 'direct_to_template', {'template': 'assessment/c01_s03_cover.html'}, name='essays-grandio'),
    url(r'^c01_s04_cover$', 'direct_to_template', {'template': 'assessment/c01_s04_cover.html'}, name='essays-solomon'),
    url(r'^c01_s05_cover$', 'direct_to_template', {'template': 'assessment/c01_s05_cover.html'}, name='essays-mulgrave'),
    url(r'^c01_s06_cover$', 'direct_to_template', {'template': 'assessment/c01_s06_cover.html'}, name='essays-applied-history'),
    
    url(r'intro-maps$', 'direct_to_template', {'template': 'assessment/intro-maps.html'}, name='intro-maps'),
    
    url(r'^estimates$', 'direct_to_template', {'template': 'under_constr.html'}, name='estimates'),

)
