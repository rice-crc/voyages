from __future__ import division, unicode_literals

import re
from builtins import str

import django
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from django.views.decorators.cache import cache_page
from past.utils import old_div

from voyages.apps.voyage.models import Nationality, Place


@cache_page(3600)
def get_nations(_):
    nations = {
        n.pk: {
            'name': n.label,
            'code': n.value
        } for n in Nationality.objects.all()
    }
    return JsonResponse(nations)


def get_ordered_places(place_query=None, translate=True):
    if place_query is None:
        place_query = Place.objects
    trans = _ if translate else (lambda x: x)
    # retrieve list of places in the system.
    places = sorted(place_query.prefetch_related('region__broad_region'),
                    key=lambda p: (p.region.broad_region.broad_region
                                   if p.region.broad_region.value != 80000 else
                                   'zzz', p.region.value, p.value))
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
            result.append({
                'type': 'broad_region',
                'order': counter,
                'pk': broad_region.pk,
                'value': -counter,
                'broad_region': trans(broad_region.broad_region)
            })
            counter += 1
        if last_region != region:
            last_region = region
            result.append({
                'type': 'region',
                'order': counter,
                'value': -counter,
                'pk': region.pk,
                'code': region.value,
                'parent': broad_region.pk,
                'region': trans(region.region)
            })
            counter += 1
        result.append({
            'type': 'port',
            'order': counter,
            'value': place.pk,
            'parent': region.pk,
            'code': place.value,
            'port': trans(place.place)
        })
    return result


class FlatPageTree:
    """
    Represents a hierarchy of flat pages.
    """

    def __init__(self, lang_set, order, parent):
        """
        The lang_set contains a dict of FlatPages indexed by language code.
        It may be empty if this item is a root or intermediary node.
        """
        self.lang_set = lang_set
        self.order = order
        self.children = []
        if parent:
            siblings = parent.children
            siblings.append(self)
            parent.children = sorted(siblings, key=lambda node: node.order)

    def get_lang_page_or_default(self, lang):
        """
        Get the page with the language specified or a default if no language
        match is found. This method returns None if self.lang_set is empty.
        """
        s = self.lang_set
        return s.get(lang,
                     s.get('en',
                           list(s.values())[0] if len(s) > 0 else None))

    def flatten(self, lang):
        """
        Creates a flat representation in the form of an array of triples
        (nest_level, page, tree_node).
        If the set of FlatPages is malformed (missing intermediary)
        pages, the flatten structure may produce jumps from levels, e.g.,
        [.. (1, page, _), (3, jumped, _) ..]
        In this case it because there is a missing FlatPage with URL
        between the 1st and 3rd levels. This FlatPage can be created
        with just a title and empty content.
        """
        items = []

        def recursive(level, node):
            page = node.get_lang_page_or_default(lang)
            if page:
                items.append((level, page, node))
            for child in node.children:
                recursive(level + 1, child)

        recursive(0, self)
        return items


def get_flat_page_tree(prefix, language=None):
    """
    Obtain a flat page tree from the given URL prefix.
    Optionally filter by the language code.
    Note that if the language filter is active not all pages
    may be returned (e.g. if there is no translation in the
    given language, the result is not included in the tree).
    """
    prefix_length = len(prefix)
    query = FlatPage.objects.filter(url__startswith=prefix)
    if language:
        query = query.filter(url__endswith=language + '/')
    pages = list(query)
    # The structure will be a dict with possibly nested dicts
    # where the keys represent parts of the URL that are separated
    # by '/'. At the leaves we store an array with triples
    # (page, order, language).
    structure = {}
    leaf_key = '__<fpage>__'
    for page in pages:
        path = [x for x in page.url[prefix_length:].split('/') if x != '']
        if len(path) < 3:
            continue
        # URL should look like
        # {prefix}/top_level/optional_nested_level/order_number/language_code/
        # There can be as many nested levels as required.
        lang = path.pop()
        order_str = path.pop()
        # order should be numeric
        order = None
        try:
            order = float(order_str)
        except Exception:
            pass
        d = structure
        for item in path:
            d = d.setdefault(item, {})
        lang_set = d.setdefault(leaf_key, [])
        lang_set.append((page, order, lang))

    def recursive_create(d, parent):
        leaf_set = d.get(leaf_key, [])
        node = FlatPageTree(
            {t[2]: t[0] for t in leaf_set},
            min([t[1] for t in leaf_set]) if len(leaf_set) > 0 else 0, parent)
        for k, v in list(d.items()):
            if k != leaf_key:
                recursive_create(v, node)
        return node

    return recursive_create(structure, None)


@cache_page(3600)
def get_flat_page_content(_, url):
    page = get_object_or_404(FlatPage, url=url)
    # Remove CDATA before we return
    content = page.content.replace("// <![CDATA[", "").replace("// ]]>", "")
    content = re.sub(r'\{\{\s*MEDIA_URL\s*\}\}',
                     settings.MEDIA_URL,
                     content,
                     flags=re.MULTILINE)
    return HttpResponse(content, 'text/html; charset=utf-8')


@cache_page(3600)
def get_flat_page_hierarchy(request, prefix):
    tree = get_flat_page_tree(prefix)
    lang = get_language()
    flat = tree.flatten(lang)

    def get_page_info(t):
        page = t[1]
        title = page.title
        url = page.url
        # If a page is marked with 'NO-CONTENT' in its content field,
        # we try to replace the page's url with its first child, so
        # that the links point to some content.
        # This method should work for multiple nested levels as well.
        node = t[2]
        while node and page and len(node.children) > 0 and len(
                page.content) < 50 and 'NO-CONTENT' in page.content:
            node = node.children[0]
            page = node.get_lang_page_or_default(lang)
            if page:
                url = page.url
        url = request.build_absolute_uri(
            reverse('common:get_flat_page_content', args=[url]))
        return {'level': t[0], 'title': title, 'url': url}

    return JsonResponse({
        'prefix': prefix,
        'items': [get_page_info(t) for t in flat]
    })


def _default_solr_value_adapter(pair):
    key = pair[0]
    val = pair[1]
    if val == '[]':
        val = ''
    if key.endswith('_partial') and val is not None:
        # This is a partial date so we map from [MM],[DD],[YYYY] to
        # [YYYY]-[MM]-[DD]
        comps = str(val).split(',')
        if len(comps) == 3:
            try:
                month = int(comps[0]) if comps[0] != '' else None
                day = int(comps[1]) if comps[1] != '' else None
                year = int(comps[2]) if comps[2] != '' else None
                if year is None:
                    val = ''
                else:
                    val = str(year)
                    if month:
                        val = val + '-' + str(month)
                    if day:
                        val = val + '-' + str(day)
            except Exception:
                pass
    return val


def get_datatable_json_result(results,
                              post,
                              field_filter=lambda _: True,
                              key_adapter=lambda t: t[0],
                              value_adapter=_default_solr_value_adapter):
    """
    Produce a JSON output that can be parsed by a paginated DataTable in the
    front-end. The argument results should be a SearchQuerySet and post should
    be a dict that contains a key tableParams with the DataTable corresponding
    parameters.
    """
    table_params = {}
    try:
        table_params = post['tableParams']
        rows_per_page = int(table_params['length'])
        current_page_num = 1 + \
            old_div(int(table_params['start']), rows_per_page)
        paginator = Paginator(results, rows_per_page)
        page = paginator.page(current_page_num)
    except Exception:
        page = results
    reponse_data = {}
    total_results = results.count()
    reponse_data['recordsTotal'] = total_results
    reponse_data['recordsFiltered'] = total_results
    reponse_data['draw'] = int(table_params.get('draw', 0))
    reponse_data['data'] = [{
        key_adapter((k, v)): value_adapter((k, v))
        for k, v in list(x.get_stored_fields().items())
        if field_filter(k)
    } for x in page]
    return JsonResponse(reponse_data)


def set_language(request, lang_code):
    """
    A wrapper around django.views.i18n.set_language suitable for an AJAX GET
    request.
    :param request: web request.
    :param lang_code: language code of the new language to use site-wise.
    :return: a plain text response with the given lang_code.
    """
    request.method = 'POST'
    request.POST = {'language': lang_code}
    django.views.i18n.set_language(request)
    return django.http.HttpResponse(lang_code, content_type="text/plain")
