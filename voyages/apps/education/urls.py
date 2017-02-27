from django.conf.urls import url

import voyages.apps.static_content.views
import voyages.apps.education.views
import django.contrib.flatpages.views

urlpatterns = [
    url(r'^$', voyages.apps.static_content.views.get_static_content,
        {'group': 'Educational Materials'}, name='index'),
    url(r'lesson-plans', voyages.apps.education.views.lessonplan, name='lesson-plans'),
    url(r'web-resources', django.contrib.flatpages.views.flatpage,
        {'url': '/education/web-resources/'}, name='web-resources')]
