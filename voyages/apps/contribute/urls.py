from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import *

# To be used later
# from voyages.apps.education.views import *

urlpatterns = patterns('',
    url(r'^$', 'voyages.apps.contribute.views.index', name='index'),   
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'contribute/voyagelogin.html'}, name='login'),
    url(r'^user_index$', 'django.views.generic.simple.direct_to_template', {'template': 'contribute/index.html'}, name='user_index'),
    url(r'^guidelines$', 'django.views.generic.simple.direct_to_template', 
                {'template': 'contribute/guidelines.html'}, name='guidelines'),
    url(r'^newuser$', 'django.views.generic.simple.direct_to_template', {'template': 'under_constr.html'}, name='newuser'),
    url(r'^logout', 'voyages.apps.contribute.views.logout_view', name='logout'),
)