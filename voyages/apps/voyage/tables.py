from __future__ import unicode_literals

import json
from builtins import range


# Usage example:
# table = get_pivot_table_advanced(
#   results,
#   'var_imp_principal_port_slave_dis_idnum',
#   'var_imp_region_voyage_begin_idnum',
#   {'embarked': 'sum(var_imp_total_num_slaves_purchased)', 'disembarked':
#   'sum(var_imp_total_slaves_disembarked)'})


def get_pivot_table_advanced(results,
                             row_field,
                             col_field,
                             cell_formula_dict,
                             range=None):
    q = results.query._clone()
    q._reset()
    q.set_limits(0, 0)
    final_query = q.build_query()
    search_kwargs = q.build_params(None)
    search_kwargs = q.backend.build_search_kwargs(final_query, **search_kwargs)
    search_kwargs['q'] = final_query
    terms = {
        'field': row_field,
        'limit': 10000,
        'facet': {
            'subcat': {
                'terms': {
                    'limit': 10000,
                    'field': col_field,
                    'facet': cell_formula_dict
                }
            }
        }
    }
    domain_filter = cell_formula_dict.pop('_filter', None)
    if domain_filter:
        terms['domain'] = {'filter': domain_filter}
    facet = {'categories': {'terms': terms}}
    if range:
        terms['type'] = 'range'
        terms.update(range)
        facet['categories'] = terms
    search_kwargs['json.facet'] = json.dumps(facet)
    response = json.loads(q.backend.conn._select(search_kwargs))
    buckets = response['facets']['categories']['buckets']
    row_data = [(x['val'], {y['val']: y
                            for y in x['subcat']['buckets']})
                for x in buckets
                if 'subcat' in x]
    return row_data


class PivotTable:

    def __init__(self,
                 row_data,
                 col_map=lambda x: x,
                 row_map=lambda x: x,
                 omit_empty=False):
        self.row_data = sorted(row_data, key=lambda r: r[0])
        # Extract the columns from row_data, eliminating duplicates.
        self.original_columns = sorted({
            header for r in self.row_data for header in list(r[1].keys())})
        self.columns = [col_map(c) for c in self.original_columns]
        self.original_rows = [r[0] for r in self.row_data]
        self.rows = [row_map(r) for r in self.original_rows]
        self.cells = [[(i, r[1][col])
                       for i, col in enumerate(self.original_columns)
                       if col in r[1]]
                      for r in self.row_data]
        default_cell_key = u'cell'
        excluded_bucket_keys = [u'val', u'count']
        zero_threshold = 0.0001

        if omit_empty:
            # Delete any column or row for which all the entries are zero/None.
            def safe_num(x):
                try:
                    return (float(x[default_cell_key])
                            if default_cell_key in x
                            else (
                                sum([float(v)
                                     for k, v in list(x.items())
                                     if k not in excluded_bucket_keys])))
                except Exception:
                    return 0

            # Delete rows that are zero-valued.
            for i in range(len(self.cells) - 1, -1, -1):
                if sum([abs(safe_num(x[1])) for x in self.cells[i]
                        ]) <= zero_threshold:
                    del self.cells[i]
                    del self.rows[i]
                    del self.original_rows[i]
            # Deleting columns is more complicated since the cells point to
            # column indices that change after deletion.
            deleted_columns = []
            for j in range(0, len(self.columns)):
                col = self.original_columns[j]
                if sum([
                        abs(safe_num(r[1][col]))
                        for r in self.row_data
                        if col in r[1]
                ]) <= zero_threshold:
                    deleted_columns.append(j)
            for k, colm in enumerate(deleted_columns):
                # The index needs to account for already deleted columns.
                del_index = colm - k
                del self.columns[del_index]
                del self.original_columns[del_index]
                # Update indices from sparse cell data and exclude those that
                # match the deleted column index.
                self.cells = [[(t[0] if t[0] < del_index else t[0] - 1, t[1])
                               for t in sparse_row
                               if t[0] != del_index]
                              for sparse_row in self.cells]

    def to_dict(self):
        return {'columns': self.columns,
                'rows': self.rows,
                'cells': self.cells}
