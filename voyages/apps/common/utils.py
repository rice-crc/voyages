import itertools
import re
import sys

from voyages.apps.voyage.models import VoyageSources
from unidecode import unidecode
import unicodecsv

empty = re.compile(r"^\s*\.?$")

def get_multi_valued_column_suffix(max_columns):
    ALPHABET = 26
    if max_columns > 2 * ALPHABET: raise Exception("Too many columns!")
    first_char = ord('a')
    single_char_limit = min(max_columns, ALPHABET)
    for i in range(0, single_char_limit):
        yield chr(first_char + i)
    max_columns -= ALPHABET
    if max_columns > 0:
        for i in range(0, max_columns):
            yield 'a' + chr(first_char + i)
            
class RowHelper:
    """
    This helper allows column access with conversion to numeric
    types and retrieve related models through values (e.g. a Place
    value code is mapped to a Place object).
    """

    cached = {}

    def __init__(self, row, error_reporting):
        self.row = row
        self.error_reporting = error_reporting
        error_reporting.next_row()

    def cint(self, field_name, allow_null=True):
        """
        Get the value of the column as an integer.
        """
        val = self.row.get(field_name)
        is_null = val is None or empty.match(val)
        if is_null:
            if not allow_null:
                self.error_reporting.report('Null value for ' + field_name)
            return None
        try:
            return int(round(float(val)))
        except Exception:
            self.error_reporting.add_error()
            if allow_null:
                return None
            raise Exception("Invalid value for int: " + str(val))

    def cfloat(self, field_name, allow_null=True):
        """
        Get the value of the column as a float.
        """
        val = self.row.get(field_name)
        is_null = val is None or empty.match(val)
        if is_null:
            if not allow_null:
                self.error_reporting.report('Null value for ' + field_name)
            return None
        try:
            return float(val)
        except Exception:
            self.error_reporting.add_error()
            if allow_null:
                return None
            raise Exception("Invalid value for float: " + str(val))

    def get(self, field_name, default=None, max_chars=None):
        """
        Get the raw value for the field in this row.
        """
        val = self.row.get(field_name, default)
        if val:
            val = val.strip()
        if max_chars and val and len(val) > max_chars:
            self.error_reporting.report('Field "' + field_name + '" is too long (>' + str(max_chars) + ' chars)')
            # Truncate the field
            val = val[:max_chars]
        return val

    def get_by_value(self, model_type, field_name, key_name = 'value', allow_null=True, manager=None, remap=None):
        """
        Gets a model object of the given type by
        using its (integer) key code.
        This method caches all entries of the model_type
        so that subsequent calls are cheap.
        """
        model_type_name = str(model_type)
        cached_cols = self.__class__.cached
        cache_key = model_type_name + '>>' + key_name
        col = cached_cols.get(cache_key)
        if manager is None:
            manager = model_type.objects
        if col is None:
            col = {str(getattr(x, key_name)): x for x in manager.all()}
            cached_cols[cache_key] = col
        src_val = self.get(field_name)
        if src_val is None or src_val == '':
            if not allow_null:
                self.error_reporting.report('Null value for ' + field_name)
            return None
        val = col.get(src_val)
        if val is None and remap is not None:
            remaped_val = remap.get(src_val)
            if remaped_val is not None:
                if isinstance(remaped_val, list):
                    for rval in remaped_val:
                        val = col.get(rval)
                        if val is not None:
                            break
                else:
                    val = col.get(remaped_val)
        if val is None:
            msg = 'Failed to locate "' + model_type_name + '" with value: "' + \
                str(src_val) + '" for field "' + field_name + '"'
            self.error_reporting.add_missing(model_type_name, src_val)
            if not allow_null:
                raise Exception(msg)
            self.error_reporting.report(msg, field_name + str(src_val))
        return val


class BulkImportationHelper:
    """
    Helper methods for bulk data importation.
    """

    def __init__(self, target_db = None):
        self.target_db = target_db if target_db else 'mysql'

    @staticmethod
    def read_to_dict(file):
        """
        Read the file and produce a DictReader where the keys are lower case.
        """

        def lower_headers(iterator):
            return itertools.chain(
                [next(iterator).decode("utf-8-sig").lower().replace("_", "").encode('utf-8')],
                iterator)

        return unicodecsv.DictReader(lower_headers(file), delimiter=',', encoding='utf-8-sig')

    @staticmethod
    def bulk_insert(model, lst, attr_key=None, manager=None):
        """
        Bulk insert model entries
        """

        print('Bulk inserting [' + str(len(lst)) + '] ' + str(model))
        if manager is None:
            manager = model.objects
        manager.bulk_create(lst, batch_size=100)
        return None if attr_key is None else \
            {getattr(x, attr_key): x for x in manager.all()}

    def delete_all(self, cursor, model):
        """
        Delete all records of the given model by running a raw query.
        """

        quote_char = self.get_quote_char()
        sql = 'DELETE FROM {0}' + model._meta.db_table + '{0}'
        sql = sql.format(quote_char)
        print(sql)
        cursor.execute(sql)

    def disable_fks(self, cursor):
        """
        Disable foreign keys temporarily so that the importation is allowed
        to produce a partially incomplete state when needed.
        """
        if self.target_db == 'mysql':
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        elif self.target_db == 'pgsql':
            # This has not been tested: the idea is that
            # the FK might be broken temporarily, but at
            # the end of the transaction they should all
            # be satisfied.
            cursor.execute("SET CONSTRAINTS ALL DEFERRED;")
        else:
            self._raise_not_supported()

    def get_quote_char(self):
        return '`' if self.target_db == 'mysql' else '"'

    def re_enable_fks(self, cursor):
        """
        Re-enable ForeignKeys after the data importation.
        """ 
        if self.target_db == 'mysql':
            # Re-enable foreign key checks.
            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        elif self.target_db == 'pgsql':
            # We expect that the constraints will be applied at the end of the transaction.
            pass
        else:
            self._raise_not_supported()

    def _raise_not_supported(self):
        raise Exception('Target db "' + self.target_db + '" not supported')


class ErrorReporting:
    """
    Helper class to report errors in importation methods.
    """

    def __init__(self):
        self.line = 0
        self.errors = 0
        self.reported = {}
        self.missing = {}

    def add_error(self):
        """
        Add 1 to the error count.
        """
        self.errors += 1

    def add_missing(self, model, search_key):
        self.missing.setdefault(model, []).append(search_key)

    def next_row(self):
        """
        Move to the next row in the import.
        """

        self.line += 1

    def reset_row(self):
        """
        Reset the row number back to zero.
        """

        self.line = 0

    def report(self, msg, key=None):
        """
        Report an error message at the current row.
        """

        self.add_error()
        if key is None:
            key = msg
        msg_count = 1 + self.reported.get(key, 0)
        self.reported[key] = msg_count + 1
        saturated = msg_count > 1
        if self.line > 0 and not saturated:
            msg = f"{msg} [{self.line}]"
        if not saturated:
            sys.stderr.write(msg + '\n')


class Trie:
    def __init__(self, excluded_chars=[' ', ',', '(', ')'], multivalued=False):
        self.trie = {}
        self._end = '_end'
        self.excluded_chars = excluded_chars
        self.multivalued = multivalued

    def add(self, key, value):
        """
        Add an entry to the tree. If multivalued, all the values will be placed
        in a list and the key will map to that list. For single-valued tries,
        only the last added entry with the same key is kept and no Exception is
        raised in case a key is re-added.
        """
        dictionary = self.trie
        has_star = False
        for letter in key:
            if letter in self.excluded_chars:
                continue
            if has_star:
                raise Exception("Our trie only accepts a single * element and it must be the last character")
            has_star = letter == '*'
            dictionary = dictionary.setdefault(letter, {})
        if self.multivalued:
            leaf = dictionary.setdefault(self._end, [])
            leaf.append(value)
        else:
            # Overwrite any existing value.
            dictionary[self._end] = value

    def get(self, key):
        """
        Look for an exact match in the Trie. If not found, None is returned. For
        multivalued tries, the return is either a list with one or more matches
        or None.
        """
        (best, _, is_exact) = self.get_longest_prefix_match(key)
        return best if is_exact else None

    def get_longest_prefix_match(self, key):
        """
        This method searches the trie and obtain the value whose key matches the
        longest prefix of the given key.
        """
        best = None
        match = ''
        dictionary = self.trie
        is_exact = True
        star_match = None
        for letter in key:
            if letter in self.excluded_chars:
                continue
            is_exact = False
            dictionary = dictionary.get(letter)
            if dictionary is None:
                break
            match += letter
            best = dictionary.get(self._end, best)
            star_match = dictionary.get('*') or star_match
            is_exact = True
        if (not is_exact or (is_exact and best is None)) and star_match is not None and self._end in star_match:
            best = star_match.get(self._end)
            is_exact = True
        return best, match, is_exact


class SourceReferenceFinder:
    """
    This helper indexes source references.
    """

    def __init__(self, all_sources = None):
        if not all_sources:
            all_sources = VoyageSources.objects.all()
        self.trie = Trie()

        for source in all_sources:
            plain = unidecode(source.short_ref).lower()
            self.trie.add(plain, source)

    def get(self, ref):
        """
        This method searches the Sources trie and obtain the
        Source whose short reference matches the longest
        prefix of the given reference.
        """
        plain = unidecode(ref).lower()
        (best, match, _) = self.trie.get_longest_prefix_match(plain)
        return best, match
