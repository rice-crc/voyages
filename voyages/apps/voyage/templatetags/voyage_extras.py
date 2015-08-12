from django import template
from django.template import Template, Context
from django.template.defaultfilters import stringfilter
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import logging

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

import re
re_has_alpha_chars = re.compile('[a-zA-Z]{2,}')

@register.filter
@stringfilter
def trans_log(val):
    """
    This filter attempts to translate a given value if it recognizes it
    as text (and not, say, HTML). Every time the translation fails to
    provide a different value, the original value is logged to the
    'trans' logger for collection.
    :param val: The value to translate.
    :return: The translated value or the original val if no suitable
    translation is found.
    """
    if not isinstance(val, basestring):
        return val
    # Heuristically check whether this looks like a string that should be translated.
    if len(val) == 0 or val[0] == '<' or not re_has_alpha_chars.match(val):
        return val
    if val.startswith('var_'):
        return val
    result = _(val)
    if result == val:
        logging.getLogger('trans').info(val)
        result += '[T]'
    return result
