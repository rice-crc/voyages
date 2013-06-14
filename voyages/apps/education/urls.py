from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


# To be used later
# from voyages.apps.education.views import *

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='education/index.html'), name='index'),
    url(r'^web-resources$', TemplateView.as_view(template_name='education/others.html'), name='others'),
)

urlpatterns += patterns('',
    url(r'^lesson-plans$', 'voyages.apps.education.views.lessonplan', name='lesson-plans'),                    
)
