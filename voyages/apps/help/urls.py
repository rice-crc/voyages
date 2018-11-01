from django.conf.urls import url
from django.views.generic import TemplateView
import voyages.apps.help.views

urlpatterns = [
    url(r'^page_sitemap', TemplateView.as_view(template_name='help/page_sitemap.html'), name='sitemap'),
    url(r'^page_demos', TemplateView.as_view(template_name='help/page_demos.html'), name='demos'),
    url(r'^page_legal', TemplateView.as_view(template_name='help/page_legal.html'), name='legal'),
    url(r'^page_demo-overview', TemplateView.as_view(template_name='help/page_demo-overview.html'), name='demo-overview'),
    url(r'^page_demo-search', TemplateView.as_view(template_name='help/page_demo-search.html'), name='demo-search'),
    url(r'^page_glossary', voyages.apps.help.views.glossary_page, name='glossary'),
    url(r'^page_faqs', voyages.apps.help.views.get_faqs, name='faqs'),
    url(r'^get_glossary_table', voyages.apps.help.views.get_glossary_table, name='get-glossary-table')]

