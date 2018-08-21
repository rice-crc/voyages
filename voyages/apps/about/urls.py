from django.conf.urls import url
from django.views.generic import TemplateView

import voyages.apps.static_content.views
import voyages.apps.about.views

urlpatterns = [
    url(r'^$', voyages.apps.static_content.views.get_static_content, {'group': 'About'}, name='index'),
    url(r'^history', TemplateView.as_view(template_name='about/history.html'), name='history'),
    url(r'^team', TemplateView.as_view(template_name='about/team.html'), name='team'),
    url(r'^data', TemplateView.as_view(template_name='about/data.html'), name='data'),
    url(r'^faq', TemplateView.as_view(template_name='about/faq.html'), name='faq'),
    url(r'^glossary', TemplateView.as_view(template_name='about/glossary.html'), name='glossary'),
    url(r'^legal', TemplateView.as_view(template_name='about/legal.html'), name='legal'),
    url(r'^acknowledgements',
        TemplateView.as_view(template_name='about/acknowledgements.html'), name='acknowledgements'),
    url(r'^origins', TemplateView.as_view(template_name='about/origins.html'), name='origins'),
    url(r'^contacts', TemplateView.as_view(template_name='about/contacts.html'), name='contacts'),

    # flatpage urls
    url(r'^flatpage/index/en', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/index/en/'}),
    url(r'^flatpage/index/pt', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/index/pt/'}),
    url(r'^flatpage/index/es', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/index/es/'}),
    url(r'^flatpage/history/en', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/history/en/'}),
    url(r'^flatpage/history/pt', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/history/pt/'}),
    url(r'^flatpage/history/es', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/history/es/'}),
    url(r'^flatpage/team/en', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/team/en/'}),
    url(r'^flatpage/team/pt', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/team/pt/'}),
    url(r'^flatpage/team/es', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/team/es/'}),
    url(r'^flatpage/data/en', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/data/en/'}),
    url(r'^flatpage/data/pt', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/data/pt/'}),
    url(r'^flatpage/data/es', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/data/es/'}),
    url(r'^flatpage/faq/en', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/faq/en/'}),
    url(r'^flatpage/faq/pt', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/faq/pt/'}),
    url(r'^flatpage/faq/es', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/faq/es/'}),
    url(r'^flatpage/glossary/en', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/glossary/en/'}),
    url(r'^flatpage/glossary/pt', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/glossary/pt/'}),
    url(r'^flatpage/glossary/es', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/glossary/es/'}),
    url(r'^flatpage/legal/en', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/legal/en/'}),
    url(r'^flatpage/legal/pt', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/legal/pt/'}),
    url(r'^flatpage/legal/es', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/legal/es/'}),
    url(r'^flatpage/acknowledgements/en', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/acknowledgements/en/'}),
    url(r'^flatpage/acknowledgements/pt', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/acknowledgements/pt/'}),
    url(r'^flatpage/acknowledgements/es', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/acknowledgements/es/'}),
    url(r'^flatpage/origins/en', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/origins/en/'}),
    url(r'^flatpage/origins/pt', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/origins/pt/'}),
    url(r'^flatpage/origins/es', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/origins/es/'}),
    url(r'^flatpage/contacts/en', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/contacts/en/'}),
    url(r'^flatpage/contacts/pt', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/contacts/pt/'}),
    url(r'^flatpage/contacts/es', voyages.apps.about.views.render_about_flatpage, {'flatpage_url': '/about/contacts/es/'}),
]
