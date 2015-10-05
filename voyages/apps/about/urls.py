from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
                       url(r'^$', 'voyages.apps.static_content.views.get_static_content', {'group': 'About'}
                           , name='index'),
                       url(r'^history$', TemplateView.as_view(template_name='about/history.html'), name='history'),
                       url(r'^team$', TemplateView.as_view(template_name='about/team.html'), name='team'),
                       url(r'^data$', TemplateView.as_view(template_name='about/data.html'), name='data'),
                       url(r'^acknowledgements$',
                           TemplateView.as_view(template_name='about/acknowledgements.html'), name='acknowledgements'),
                       url(r'^origins$', TemplateView.as_view(template_name='about/origins.html'), name='origins'),
                       url(r'^contacts$', TemplateView.as_view(template_name='about/contacts.html'), name='contacts'),
                       )

