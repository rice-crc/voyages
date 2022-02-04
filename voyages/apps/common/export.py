from __future__ import unicode_literals

from builtins import str

import xlwt
from django.http import HttpResponse


def download_xls(header_rows, data_set, row_header_columns=None):
    """
    Generates an XLS file with the given data.
    :param header_rows: An array of header rows, with each row being an array
    of pairs (header label, column span)
    :param data_set: Tabular data in the format [[r_1c_1, r_1c_2, ..., r_1c_N],
    ..., [r_Mc_1, r_Mc_2, ..., r_Mc_N]]
    :param row_header_columns: a collection of columns that form the row
    headers, each cell being a pair (value, rowspan)
    :return: An HttpResponse containing the XLS file.
    """
    if row_header_columns is None:
        row_header_columns = []
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=data.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Data")

    header_style = xlwt.XFStyle()
    number_style = xlwt.XFStyle()
    number_style.alignment.horz = number_style.alignment.HORZ_RIGHT

    # Write headers.
    row_index = 0
    for row in header_rows:
        col_index = len(row_header_columns)
        for pair in row:
            ws.write(row_index, col_index, str(pair[0]), header_style)
            if pair[1] > 1:
                ws.merge(row_index, row_index, col_index,
                         col_index + pair[1] - 1)
            col_index += pair[1]
        row_index += 1

    # Helper to keep track of header row column indices.
    row_header_data = []
    for rhc in row_header_columns:
        sparse_column = {}
        row_header_index = row_index
        for cell in rhc:
            sparse_column[row_header_index] = cell
            row_header_index += cell[1]
        row_header_data.append(sparse_column)
    # Write tabular data.
    for row in data_set:
        # TODO: use XLSX format that allows more rows!
        if row_index == 65536:
            break
        col_index = 0
        for rhd in row_header_data:
            if row_index in rhd:
                pair = rhd[row_index]
                ws.write(row_index, col_index, str(pair[0]), header_style)
                if pair[1] > 1:
                    ws.merge(row_index, row_index + pair[1] - 1, col_index,
                             col_index)
            col_index += 1
        for cell in row:
            ws.write(row_index, col_index, cell, number_style)
            col_index += 1
        row_index += 1

    wb.save(response)
    return response
