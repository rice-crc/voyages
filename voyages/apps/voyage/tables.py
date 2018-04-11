from django.utils.translation import ugettext_lazy as _
import json

def get_pivot_table(results, row_field, col_field, cell_formula):
    return get_pivot_table_advanced(results, row_field, col_field, {'cell': cell_formula})

# Usage example:
# table = get_pivot_table_advanced(
#   results,
#   'var_imp_principal_port_slave_dis_idnum',
#   'var_imp_region_voyage_begin_idnum',
#   {'embarked': 'sum(var_imp_total_num_slaves_purchased)', 'disembarked': 'sum(var_imp_total_slaves_disembarked)'})

def get_pivot_table_advanced(results, row_field, col_field, cell_formula_dict):
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
                    'facet': cell_formula_dict}
            }
        }
    }
    filter = cell_formula_dict.pop('_filter', None)
    if filter:
        terms['domain'] = { 'filter': filter }
    search_kwargs['json.facet'] = json.dumps({ 'categories': { 'terms': terms } })
    response = json.loads(q.backend.conn._select(search_kwargs))
    buckets = response['facets']['categories']['buckets']
    formula_keys = [key for key in cell_formula_dict.keys() if not key.startswith('_')]
    row_data = [(x['val'], {y['val']: y for y in x['subcat']['buckets']}) for x in buckets]
    return row_data

class PivotTable():
    def __init__(self, row_data, col_map=lambda x: x, row_map=lambda x: x, sparse=True):
        self.row_data = sorted(row_data, key=lambda r: r[0])
        self.original_columns = sorted(set([header for r in self.row_data for header in r[1].keys()]))
        self.columns = [col_map(c) for c in self.original_columns]
        self.original_rows = [r[0] for r in self.row_data]
        self.rows = [row_map(row_header) for row_header in self.original_rows]
        if sparse:
            self.cells = [[(i, r[1][col]) for i, col in enumerate(self.original_columns) if col in r[1]] for r in self.row_data]
        else:
            self.cells = [[r[1].get(col) for col in self.original_columns] for r in self.row_data]

    def to_dict(self):
        return {'columns': self.columns, 'rows': self.rows, 'cells': self.cells}