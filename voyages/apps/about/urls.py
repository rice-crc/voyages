from django.conf.urls import url
from django.views.generic import TemplateView

import voyages.apps.static_content.views
import voyages.apps.about.views

urlpatterns = [
    url(r'^about', TemplateView.as_view(template_name='index.html'), name='about'),
]