from django import template

register = template.Library()

@register.filter
def multiply(number, *args, **kwargs):
    return number * 2