from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from voyages.apps.contribute.forms import LoginForm

urlpatterns = patterns('',
    url(r'^$', 'voyages.apps.contribute.views.index', name='index'),   
    
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'contribute/voyagelogin.html', 'authentication_form':LoginForm}, name='login'),
    
    url(r'^guidelines$', TemplateView.as_view(template_name='contribute/guidelines.html'), name='guidelines'),
    url(r'^newuser$', TemplateView.as_view(template_name='under_constr.html'), name='newuser'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'^change-password$', 'django.contrib.auth.views.password_change', 
        {'post_change_redirect': 'change-password-done' }, name="password-change"),
    url(r'^change-password-done$', 'django.contrib.auth.views.password_change_done', {
        'template_name': 'contribute/password_change_done.html'}, name="password-change-done")
)
