from django.conf.urls import url
from django.views.generic import TemplateView

import voyages.apps.assessment.views
import voyages.apps.static_content.views

urlpatterns = [
    url(r'^c(?P<chapternum>\d{2})_s(?P<sectionnum>\d{2})_p(?P<pagenum>\d{2})',
        voyages.apps.assessment.views.get_page, name='get-page'),
    url(r'^$', voyages.apps.static_content.views.get_static_content, {'group': 'Assessment'}, name='index'),
    url(r'^essays$', TemplateView.as_view(template_name='assessment/c01_base.html'), name='essays'),
    
    url(r'^c01_s03_cover', TemplateView.as_view(template_name='assessment/c01_s03_cover.html'), name='essays-grandio'),
    url(r'^c01_s04_cover', TemplateView.as_view(template_name='assessment/c01_s04_cover.html'), name='essays-solomon'),
    url(r'^c01_s05_cover', TemplateView.as_view(template_name='assessment/c01_s05_cover.html'), name='essays-mulgrave'),
    url(r'^c01_s06_cover', TemplateView.as_view(template_name='assessment/c01_s06_cover.html'), name='essays-applied-history'),
    
    url(r'intro-maps', TemplateView.as_view(template_name='assessment/intro-maps.html'), name='intro-maps'),
    
    url(r'^estimates', voyages.apps.assessment.views.get_estimates, name='estimates'),

    url(r'^permalink', voyages.apps.assessment.views.get_permanent_link, name='permanent-link')]
