from __future__ import unicode_literals

from django.conf.urls import url

import voyages.apps.static_content.views

urlpatterns = [
    url(r'^$',
        voyages.apps.static_content.views.get_static_content,
        name='index'),
]
