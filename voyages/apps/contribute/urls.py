from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import *

# To be used later
# from voyages.apps.education.views import *

urlpatterns = patterns('',
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'contribute/voyagelogin.html'}, name='login'),
    url(r'^index$', 'voyages.apps.contribute.views.index', name='index'),
    url(r'^guidelines$', 'django.views.generic.simple.direct_to_template', 
                {'template': 'contribute/guidelines.html'}, name='guidelines'),
    url(r'^newuser$', 'django.views.generic.simple.direct_to_template', {'template': 'under_constr.html'}, name='newuser'),
)
