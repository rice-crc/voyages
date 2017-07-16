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
    search_kwargs['json.facet'] = "{categories: {terms: {field: '" + row_field + \
        "', facet: {subcat: {terms: {field: '" + col_field + "', facet: " + json.dumps(cell_formula_dict) + "}}}}}}"
    response = json.loads(q.backend.conn._select(search_kwargs))
    buckets = response['facets']['categories']['buckets']
    if len(cell_formula_dict) == 1:
        cell_key = cell_formula_dict.keys()[0]
        row_data = [(x['val'], {y['val']: y[cell_key] for y in x['subcat']['buckets']}) for x in buckets]
    else:
        row_data = [(x['val'], {y['val']: {k: y[k] for k in cell_formula_dict.keys()} for y in x['subcat']['buckets']})
            for x in buckets]
    return row_data

class PivotTable():
    def __init__(self, row_data, col_map=lambda x: x, row_map=lambda x: x, sparse=True):
        self.row_data = row_data
        original_columns = set([header for r in row_data for header in r[1].keys()])
        self.columns = [col_map(c) for c in original_columns]
        self.rows = [row_map(r[0]) for r in row_data]
        if sparse:
            self.cells = [[(i, r[1][col]) for i, col in enumerate(original_columns) if col in r[1]] for r in row_data]
        else:
            self.cells = [[r[1].get(col) for col in original_columns] for r in row_data]