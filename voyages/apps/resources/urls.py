from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# To be used later
# from voyages.apps.resources.views import *

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='resources/index.html'), name='index'),
    #handle all cases for now
    url(r'^images$', 'voyages.apps.resources.views.get_all_images', name='images'),
    url(r'^images/category/(?P<category>\w+)$', 'voyages.apps.resources.views.get_images_category', name='images-category'),
    url(r'^images/category/(?P<category>\w+)/(?P<page>\d{1,3})$', 'voyages.apps.resources.views.get_images_category_detail', name='images-category-detail'),
    url(r'^names-database', TemplateView.as_view(template_name='under_constr.html'), name='origins'),
    url(r'^[\w\.\-]+\$', TemplateView.as_view(template_name='under_constr.html')),
)
