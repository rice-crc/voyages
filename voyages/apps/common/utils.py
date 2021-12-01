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
        if max_chars and len(val) > max_chars:
            self.error_reporting.report('Field ' + field_name + ' is too long (>' + str(max_chars) + ' chars)')
        return val

    def get_by_value(self, model_type, field_name, key_name = 'value', allow_null=True, manager=None):
        """
        Gets a model object of the given type by
        using its (integer) key code.
        This method caches all entries of the model_type
        so that subsequent calls are cheap.
        """
        model_type_name = str(model_type)
        cached_cols = self.__class__.cached
        col = cached_cols.get(model_type_name)
        if manager is None:
            manager = model_type.objects
        if col is None:
            col = {getattr(x, key_name): x for x in manager.all()}
            cached_cols[model_type_name] = col
        ival = self.cint(field_name, allow_null)
        if ival is None:
            return None
        val = col.get(ival)
        if val is None:
            msg = 'Failed to locate "' + model_type_name + '" with value: ' + \
                str(ival) + ' for field "' + field_name + '"'
            if not allow_null:
                raise Exception(msg)
            self.error_reporting.report(msg, field_name + str(ival))
        return val


class BulkImportationHelper:
    """
    Helper methods for bulk data importation.
    """

    def __init__(self, target_db):
        self.target_db = target_db

    @staticmethod
    def read_to_dict(file):
        """
        Read the file and produce a DictReader where the keys are lower case.
        """

        def lower_headers(iterator):
            return itertools.chain(
                [next(iterator).decode("utf-8-sig").lower().replace("_", "").encode('utf-8')],
                iterator)

        return unicodecsv.DictReader(lower_headers(file), delimiter=',', encoding='utf-8')

    @staticmethod
    def bulk_insert(model, lst, attr_key=None, manager=None):
        """
        Bulk insert model entries
        """

        print('Bulk inserting ' + str(model))
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

    def add_error(self):
        """
        Add 1 to the error count.
        """
        self.errors += 1

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
            msg = '[' + str(self.line) +'] ' + msg
        if not saturated:
            sys.stderr.write(msg + '\n')


class SourceReferenceFinder:
    """
    This helper indexes source references.
    """

    @staticmethod
    def is_char_excluded(letter):
        """
        Determine if the character should be excluded when matching sources.
        """
        return letter in (' ', ',')

    def __init__(self):
        all_sources = VoyageSources.objects.all()
        trie = {}
        self._end = '_end'

        def add_to_trie(_, value):
            dictionary = trie
            for letter in plain:
                if self.__class__.is_char_excluded(letter):
                    continue
                dictionary = dictionary.setdefault(letter, {})
            dictionary[self._end] = value

        for source in all_sources:
            plain = unidecode(source.short_ref).lower()
            add_to_trie(plain, source)
        self.trie = trie

    def get(self, ref):
        """
        This method searches the Sources trie and obtain the
        Source whose short reference matches the longest
        prefix of the given reference.
        """
        best = None
        match = ''
        dictionary = self.trie
        plain = unidecode(ref).lower()
        for letter in plain:
            if self.__class__.is_char_excluded(letter):
                continue
            dictionary = dictionary.get(letter)
            if dictionary is None:
                break
            match += letter
            best = dictionary.get(self._end, best)
        return best, match
