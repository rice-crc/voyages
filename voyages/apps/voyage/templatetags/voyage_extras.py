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


@register.filter
@stringfilter
def get_year_value(value):
    """ use the django template loader and response object to spit
    out rendered content
    """
    try:
        ret = value.split(",")[2]
    except:
        ret = ""
    return ret


@register.filter
@stringfilter
def translate_source_name(label_name):
    print label_name
    ret = ""
    for i in label_name.split("_"):
        ret += " " + i.capitalize()
    return ret


@register.filter
@stringfilter
def create_page_name(name, number):
    return str(name + "-" + str(number))