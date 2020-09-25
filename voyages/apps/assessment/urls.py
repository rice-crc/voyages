from django.conf.urls import url
from django.views.generic import TemplateView

import voyages.apps.assessment.views
import voyages.apps.static_content.views

urlpatterns = [
    url(r'^c(?P<chapternum>\d{2})_s(?P<sectionnum>\d{2})_p(?P<pagenum>\d{2})$',
        voyages.apps.assessment.views.get_page, name='get-page'),
    url(r'^$', voyages.apps.static_content.views.get_static_content, {'group': 'Assessment'}, name='index'),
    
    url(r'^estimates', voyages.apps.assessment.views.get_estimates, name='estimates'),

    url(r'^permalink', voyages.apps.assessment.views.get_permanent_link, name='permanent-link')]
