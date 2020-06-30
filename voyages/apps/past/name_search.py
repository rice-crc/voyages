# Levenshtein-distance based search with ranked results.
# https://en.wikipedia.org/wiki/Levenshtein_distance

import threading
import unicodedata
import heapq
import Levenshtein_search
from voyages.apps.past.models import Enslaved

# function obtained from https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    return str(text.lower())

class NameSearchCache:
    _loaded = False
    _lock = threading.Lock()
    _index = None
    _name_key = {}

    @classmethod
    def search(cls, name, max_cost = 3, max_results = 100):
        res = cls.search_full(name, max_cost, max_results)
        return [id for x in res for id in x[0]]

    @classmethod
    def search_full(cls, name, max_cost, max_results):
        res = sorted(Levenshtein_search.lookup(0, strip_accents(name), max_cost), key=lambda x: x[1])
        return [(cls._name_key[x[0]], x[1], x[0]) for x in res[0:max_results]]

    @classmethod
    def load(cls, force_reload=False):
        with cls._lock:
            if not force_reload and cls._loaded: return
            Levenshtein_search.clear_wordset(0)
            cls._name_key = {}
            all_names = set()
            q = Enslaved.objects.values_list('enslaved_id', 'documented_name', 'name_first', 'name_second', 'name_third')
            for item in q:
                ns = set([strip_accents(item[i]) for i in range(1, 4) if item[i] is not None])
                all_names.update(ns)
                id = item[0]
                for name in ns:
                    ids = cls._name_key.setdefault(name, [])
                    ids.append(id)
            Levenshtein_search.populate_wordset(0, list(all_names))
            cls._loaded = True
