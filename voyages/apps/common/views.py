from django.contrib.flatpages.models import FlatPage
from django.shortcuts import render
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from voyages.apps.voyage.models import Place
from django.http import Http404
import django

def get_ordered_places(place_query=None, translate=True):
    if place_query is None:
        place_query = Place.objects
    trans = _ if translate else (lambda x: x)
    # retrieve list of places in the system.
    places = sorted(place_query.prefetch_related('region__broad_region'),
                    key=lambda p: (
                        p.region.broad_region.broad_region if p.region.broad_region.value != 80000 else 'zzz',
                        p.region.value,
                        p.value))
    result = []
    last_broad_region = None
    last_region = None
    counter = 0
    for place in places:
        region = place.region
        broad_region = region.broad_region
        counter += 1
        if last_broad_region != broad_region:
            last_broad_region = broad_region
            result.append({'type': 'broad_region',
                           'order': counter,
                           'pk': broad_region.pk,
                           'value': -counter,
                           'broad_region': trans(broad_region.broad_region)})
            counter += 1
        if last_region != region:
            last_region = region
            result.append({'type': 'region',
                           'order': counter,
                           'value': -counter,
                           'pk': region.pk,
                           'code': region.value,
                           'parent': broad_region.pk,
                           'region': trans(region.region)})
            counter += 1
        result.append({'type': 'port',
                       'order': counter,
                       'value': place.pk,
                       'parent': region.pk,
                       'code': place.value,
                       'port': trans(place.place)})
    return result


def _get_flatpage(url, lang):
    page = None
    try:
        localized_url = url + ((lang + '/') if lang else '')
        page = FlatPage.objects.get(url=localized_url)
    except:
        pass
    return page

def render_locale_flatpage(request, template_path, flatpage_url):
    lang = get_language()
    page = _get_flatpage(flatpage_url, lang)
    if not page and lang != 'en':
        page = _get_flatpage(flatpage_url, 'en')
    if not page:
        page = _get_flatpage(flatpage_url, None)
    if not page:
        raise Http404("Your selected flatpage is not found")
    return render(request, template_path, {'flatpage': page})

def set_language(request, lang_code):
    """
    A wrapper around django.views.i18n.set_language suitable for an AJAX GET request.
    :param request: web request.
    :param lang_code: language code of the new language to use site-wise.
    :return: a plain text response with the given lang_code.
    """
    request.method = 'POST'
    request.POST = {'language': lang_code}
    django.views.i18n.set_language(request)
    return django.http.HttpResponse(lang_code, content_type="text/plain")
