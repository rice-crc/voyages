def download_xls(header_rows, data_set, header_col_offset=0):
    """
    Generates an XLS file with the given data.
    :param header_rows: An array of header rows, with each row being an array of pairs (header label, column span)
    :param data_set: Tabular data in the format [[r_1c_1, r_1c_2, ..., r_1c_N], ..., [r_Mc_1, r_Mc_2, ..., r_Mc_N]]
    :return: An HttpResponse containing the XLS file.
    """
    import xlwt
    from django.http import HttpResponse
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=data.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Data")

    header_style = xlwt.XFStyle()
    number_style = xlwt.XFStyle()
    number_style.alignment.horz = number_style.alignment.HORZ_RIGHT

    # Write headers.
    row_index = 0
    for row in header_rows:
        col_index = header_col_offset
        for pair in row:
            ws.write(row_index, col_index, pair[0], header_style)
            if pair[1] > 1:
                ws.merge(row_index, row_index, col_index, col_index + pair[1] - 1)
            col_index += pair[1]
        row_index += 1

    # Write tabular data.
    for row in data_set:
        col_index = 0
        for cell in row:
            ws.write(row_index, col_index, cell, number_style if col_index > 0 else header_style)
            col_index += 1
        row_index += 1

    wb.save(response)
    return response
