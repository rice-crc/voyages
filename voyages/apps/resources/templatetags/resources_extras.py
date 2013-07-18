from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

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