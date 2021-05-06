from __future__ import unicode_literals

from django import template
from django.template.defaultfilters import stringfilter

from voyages.apps.common.filters import trans_log

register = template.Library()
register.filter('trans_log', trans_log)


@register.filter
@stringfilter
def get_year_value(value):
    """ use the django template loader and response object to spit
    out rendered content
    """
    try:
        ret = value.split(",")[2]
    except Exception:
        ret = ""
    return ret


@register.filter
def modulo(num, val):
    return num % val


@register.filter
def spaces_to_underscores(words):
    return "_".join(words.split(" "))


@register.filter
def decode_language(code):
    xlate = {
        "en": "English",
        "fr": "French",
        "de": "German",
        "pt": "Portuguese",
        "nl": "Dutch",
        "la": "Latin",
        "es": "Spanish"
    }
    if code in xlate:
        return xlate[code]
    return None
