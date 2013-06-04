# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, RequestContext
from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout 

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('contribute:user_index'))  
    else:
        return HttpResponseRedirect(reverse('contribute:login'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('contribute:login'))
