from django import template
from django.template import Template, Context
from django.template.defaultfilters import stringfilter
from django.conf import settings

register = template.Library()

@register.filter
@stringfilter
def parse_blocks(value):
    """ use the django template loader and response object to spit 
    out rendered content
    """
    t = Template(value)
    c = Context({ 'MEDIA_URL': settings.MEDIA_URL })
    return t.render(c)

