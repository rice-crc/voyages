# Create your views here.
from django.http import Http404
from django.template import TemplateDoesNotExist, Context, loader
from django.views.generic.simple import direct_to_template

def index(request):
    try:
        return direct_to_template(request, template="index.html")
    except TemplateDoesNotExist:
        raise Http404()