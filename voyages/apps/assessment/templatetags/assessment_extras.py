from __future__ import unicode_literals

from builtins import range

from django import template

from voyages.apps.common.filters import trans_log

register = template.Library()
register.filter('trans_log', trans_log)


@register.filter
def multiply(number, *_):
    return number * 2


@register.filter
def get_range(value):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
        <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
    <li>0. Do something</li>
    <li>1. Do something</li>
    <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return list(range(value))


@register.filter
def get_item(collection, index):
    """
    Filter - returns collection[index].
    :param lst: the list or dictionary.
    :param index: the index to access.
    :return: collection[index].
    """
    return collection[index]
