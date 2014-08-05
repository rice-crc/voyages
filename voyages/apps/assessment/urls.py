from django.conf import settings
from django.conf.urls import *
from django.views.generic import TemplateView


urlpatterns = patterns('',
     # for both sections 1 and 2  
     url(r'^c(?P<chapternum>\d{2})_s(?P<sectionnum>\d{2})_p(?P<pagenum>\d{2})$','voyages.apps.assessment.views.get_page', name='get-page'), 
)

urlpatterns += patterns('',
    url(r'^$', 'voyages.apps.static_content.views.get_static_content', {'group': 'Assessment'}, name='index'),
    url(r'^essays$', TemplateView.as_view(template_name='assessment/c01_base.html'), name='essays'),
    
    url(r'^c01_s03_cover$', TemplateView.as_view(template_name='assessment/c01_s03_cover.html'), name='essays-grandio'),
    url(r'^c01_s04_cover$', TemplateView.as_view(template_name='assessment/c01_s04_cover.html'), name='essays-solomon'),
    url(r'^c01_s05_cover$', TemplateView.as_view(template_name='assessment/c01_s05_cover.html'), name='essays-mulgrave'),
    url(r'^c01_s06_cover$', TemplateView.as_view(template_name='assessment/c01_s06_cover.html'), name='essays-applied-history'),
    
    url(r'intro-maps$', TemplateView.as_view(template_name='assessment/intro-maps.html'), name='intro-maps'),
    
    url(r'^estimates$', TemplateView.as_view(template_name='under_constr.html'), name='estimates'),

)
