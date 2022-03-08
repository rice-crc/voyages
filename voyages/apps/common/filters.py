from __future__ import unicode_literals

import logging
import re

from django import template
from django.conf import settings
from django.core import serializers
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from past.builtins import basestring

logger = logging.getLogger('trans')
register = template.Library()
re_has_alpha_chars = re.compile(r'.*[a-zA-Z\.]{2,}')


@register.filter
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
    if not isinstance(val, basestring) or len(val) == 0:
        return val
    # Heuristically check whether this looks like a string that should be
    # translated.
    if re_has_alpha_chars.match(val) and not val.startswith('var_'):
        result = _(val)
    else:
        result = val
    if result == val:
        without_line_break = val.replace('\n', ' ').replace('\r', ' ')
        tmp = _(without_line_break)
        if tmp != without_line_break:
            result = tmp
    log = False
    if result == val and settings.I18N_HELPER_DEBUG:
        log = True
        result = result[:-7] + '[T]</div>'
    if log:
        logger.info(val.replace('\n', ' ').replace('\r', ' '))
    return mark_safe(result)


@register.filter
def jsonify(lst):
    return mark_safe(serializers.serialize('json', lst))


@register.filter
def replace_star(value, arg):
    return value.replace("*", arg)
