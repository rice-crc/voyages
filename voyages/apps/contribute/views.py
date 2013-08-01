# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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
        return render(request, "contribute/index.html")
    else:
        return HttpResponseRedirect(reverse('contribute:login'))
