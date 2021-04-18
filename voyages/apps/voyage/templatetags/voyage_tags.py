from __future__ import unicode_literals

import re
from builtins import str

from django import template
from django.conf import settings

numeric_test = re.compile(r"^\d+$")
register = template.Library()


def getattribute(value, arg):

    """Gets an attribute of an object dynamically from a string name"""
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and arg in value:
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID


register.filter('getattribute', getattribute)


def filtersource(value):
    sources = value
    result = ""
    for source in sources:
        try:
            ref = source.split("<>");
            result += "<div class='source_entry'>" + ref[0] + "</div><span class='source_full_ref hidden'>" \
                      + ref[1] + "</span>"
        except IndexError:
            continue
    return result


register.filter('filtersource', filtersource)


def percentage(value):
    return format(value, "%")
register.filter('percentage', percentage)
