# Levenshtein-distance based search with ranked results.
# https://en.wikipedia.org/wiki/Levenshtein_distance

import threading
import unicodedata
import heapq
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
    text = text.decode("utf-8")
    return str(text)

LEAF_CHAR = '\0'

class _Node:
    def __init__(self, parent, char):
        self.map = {}
        self.parent = parent
        self.char = char

    def getValue(self):
        s = '' if self.parent is None else self.parent.getValue()
        if self.char != LEAF_CHAR:
            s += self.char
        return s
    
    def isLeaf(self):
        return LEAF_CHAR in self.map

    def setdefaultChar(self, char):
        m = self.map
        if char in m:
            return m[char]
        added = _Node(self, char)
        m[char] = added
        return added
    
    def setLeaf(self):
        if not LEAF_CHAR in self.map:
            self.map[LEAF_CHAR] = _Node(self, LEAF_CHAR)

def process_name(name):
    return strip_accents(name).lower()

class NameSearchIndex:
    def __init__(self):
        self._root = _Node(None, LEAF_CHAR)
    
    def add(self, name):
        name = process_name(name)
        node = self._root
        for c in name:
            node = node.setdefaultChar(c)
        node.setLeaf()
        return name

    def search(self, name, max_cost, max_results):
        """
        Search the name Trie for the given name, considering
        the Levenshtein distance.
        """
        start = (0, 0, 0, self._root)
        queue = [start]
        name = process_name(name)
        results = set()

        def add_to_queue(cost, pos, trie_del, node):
            if trie_del <= 2:
                heapq.heappush(queue, (cost, pos, trie_del, node))

        while len(queue) > 0 and len(results) < max_results:
            (cost, pos, trie_del, node) = heapq.heappop(queue)
            if cost > max_cost: break
            if pos < len(name):
                c = name[pos]
                for char, child in node.map.items():
                    if char == LEAF_CHAR: continue
                    # Substitution of a character from the search, or match when char == c.
                    match = 1 if char != c else 0
                    add_to_queue(cost + match, pos + 1, trie_del + match, child)
                    # Omission of a character from the trie.
                    add_to_queue(cost + 1, pos, trie_del + 1, child)
                # Omission of a character from the search string.
                add_to_queue(cost + 1, pos + 1, trie_del, node)
            else:
                # This is the end of the search string.
                if node.isLeaf():
                    val = node.getValue()
                    if val not in results:
                        results.add(val)
                        yield val
                # Expand children of the node.
                for char, child in node.map.items():
                    if char == LEAF_CHAR: continue
                    add_to_queue(cost + 1, pos, trie_del + 1, child)

class NameSearchCache:
    _loaded = False
    _lock = threading.Lock()
    _index = None
    _map = {}

    @classmethod
    def search(cls, name, max_cost = 3, max_results = 100):
        names = cls._index.search(name, max_cost, max_results)
        for name in names:
            ids = cls._map.get(name)
            if ids:
                for id in ids: yield id

    @classmethod
    def load(cls, force_reload=False):
        def process_row(row):
            (id, documented_name, name_1, name_2, name_3) = row
            names = [documented_name]
            if name_1:
                names.append(name_1)
            if name_2:
                names.append(name_2)
            if name_3:
                names.append(name_3)
            return (id, names)

        with cls._lock:
            if not force_reload and cls._loaded: return
            # Fetch all names and index them.
            all_names = [process_row(r) for r in Enslaved.objects.values_list('enslaved_id', 'documented_name', 'name_first', 'name_second', 'name_third')]
            index = NameSearchIndex()
            map = {}
            for (id, names) in all_names:
                for name in names:
                    name = index.add(name)
                    ids = map.setdefault(name, [])
                    ids.append(id)
            cls._index = index
            cls._map = map
