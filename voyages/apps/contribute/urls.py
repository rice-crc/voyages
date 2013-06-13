from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import *

urlpatterns = patterns('',
    url(r'^$', 'voyages.apps.contribute.views.index', name='index'),   
    
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'contribute/voyagelogin.html'}, name='login'),
    url(r'^user_index$', 'voyages.apps.contribute.views.user_index', name='user_index'),
    
    url(r'^guidelines$', 'django.views.generic.simple.direct_to_template', 
                {'template': 'contribute/guidelines.html'}, name='guidelines'),
    url(r'^newuser$', 'django.views.generic.simple.direct_to_template', {'template': 'under_constr.html'}, name='newuser'),
    url(r'^logout', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'^change-password$', 'django.contrib.auth.views.password_change', 
        {'post_change_redirect': 'change-password-done' }, name="password-change"),
    url(r'^change-password-done$', 'django.contrib.auth.views.password_change_done', {
    'template_name': 'contribute/password_change_done.html'}, name="password-change-done")
)