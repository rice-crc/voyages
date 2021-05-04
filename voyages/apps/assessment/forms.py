from __future__ import absolute_import, unicode_literals

from builtins import map, str

from django import forms
from django.utils.translation import ugettext_lazy as _

from .globals import table_cells, table_columns, table_rows


def extract(x):
    return (str(x[0]), x[1][0])


class EstimateSelectionForm(forms.Form):
    row_choices = list(map(extract, enumerate(table_rows)))
    rows = forms.ChoiceField(
        label=_('Rows'), choices=row_choices, initial=[row_choices[0][1]])
    rows.initial = row_choices[0][0]

    col_choices = list(map(extract, enumerate(table_columns)))
    columns = forms.ChoiceField(
        label=_('Columns'), choices=col_choices, initial=[col_choices[1][1]])
    columns.initial = col_choices[1][0]

    cell_choices = list(map(extract, enumerate(table_cells)))
    cells = forms.ChoiceField(
        label=_('Cells'), choices=cell_choices, initial=[cell_choices[1][1]])
    cells.initial = cell_choices[1][0]
    include_empty = forms.BooleanField(
        label=_('Include empty'), required=False, initial=False)


class EstimateYearForm(forms.Form):
    frame_from_year = forms.IntegerField(
        label=_('From'),
        widget=forms.TextInput(attrs={'class': "short_field_white"}))
    frame_to_year = forms.IntegerField(
        label=_('To'),
        widget=forms.TextInput(attrs={'class': "short_field_white"}))
