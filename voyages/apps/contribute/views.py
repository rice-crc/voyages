# Create your views here.
from django.template import TemplateDoesNotExist, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

def index(request):
    """
    Handles the redirection when user attemps to login
    Display the user index page if the user is already authenticated
    Or return to the login page if the user has not logged in yet
    
    ** Context **
    ``RequestContext``
    
    ** Templates **
    :template:`contribute/index.html`
    :template:`contribute/voyagelogin.html`
    """
    if request.user.is_authenticated():
        return render_to_response("contribute/index.html", {},
                              context_instance=RequestContext(request))  
    else:
        return HttpResponseRedirect(reverse('contribute:login'))
