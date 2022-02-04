from __future__ import unicode_literals

from django.conf.urls import url

from voyages.apps.common.views import (get_flat_page_content,
                                       get_flat_page_hierarchy, get_nations)

urlpatterns = [
    url(r'^getflatpage(?P<url>.+)',
        get_flat_page_content,
        name='get_flat_page_content'),
    url(r'^flatpagehierarchy(?P<prefix>.+)',
        get_flat_page_hierarchy,
        name='get_flat_page_hierarchy'),
    url(r'nations', get_nations, name='get_nations')
]
