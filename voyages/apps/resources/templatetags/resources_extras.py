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
    except:
        ret = ""
    return ret


@register.filter
def modulo(num, val):
    return num % val

@register.filter
def spaces_to_underscores(str):
    return "_".join(str.split(" "))

@register.filter
def decode_language(code):
    if code == "en":
        return "English"
    if code == "fr":
        return "French"
    if code == "de":
        return "German"
    if code == "pt":
        return "Portuguese"
    if code == "nl":
        return "Dutch"
    if code == "la":
        return "Latin"
    if code == "es":
        return "Spanish"