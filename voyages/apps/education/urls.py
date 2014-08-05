from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


# To be used later
# from voyages.apps.education.views import *

urlpatterns = patterns('',
                       url(r'^$', 'voyages.apps.static_content.views.get_static_content',
                           {'group': 'Educational Materials'}, name='index'),
                       )

urlpatterns += patterns('',
                        url(r'^lesson-plans$', 'voyages.apps.education.views.lessonplan', name='lesson-plans'),
                        )
urlpatterns += patterns('django.contrib.flatpages.views',
                        url(r'^web-resources', 'flatpage', {'url': '/education/web-resources/'}, name='web-resources'),
                        )