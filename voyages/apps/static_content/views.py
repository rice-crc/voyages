from __future__ import unicode_literals

from django.shortcuts import render

from .models import ContentPage

group_templates = {
    "Voyage": "voyages-index.html",
    "Assessment": "assessment-index.html",
    "Resources": "resources-index.html",
    "About": "about-index.html"
}


def get_static_content(request, group=None):
    """
    View to show appropriate landing page
    :param request: current request
    :param group: group (if empty, main landing page)
    :return: render
    """

    if group is None:
        # It's main landing page
        objects = ContentPage.objects.filter(
            group__name="Main").order_by('order')
        template = "static_content/index.html"
    else:
        objects = ContentPage.objects.filter(
            group__name=group).order_by('order')
        template = "static_content/" + group_templates[group]

    return render(request, template, {'objs': objects})
