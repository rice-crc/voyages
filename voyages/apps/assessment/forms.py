from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import *
import globals


class EstimateSelectionForm(forms.Form):
    lambda_fun = lambda x: (str(x[0]), x[1][0])

    row_choices = map(lambda_fun, enumerate(globals.table_rows))
    print row_choices
    rows = forms.ChoiceField(label=_('Rows'), choices=row_choices, initial=[row_choices[0][1]])
    rows.initial = row_choices[0][0]

    col_choices = map(lambda_fun, enumerate(globals.table_columns))
    columns = forms.ChoiceField(label=_('Columns'), choices=col_choices, initial=[col_choices[1][1]])
    columns.initial = col_choices[1][0]

    cell_choices = map(lambda_fun, enumerate(globals.table_cells))
    cells = forms.ChoiceField(label=_('Cells'), choices=cell_choices, initial=[cell_choices[1][1]])
    cells.initial = cell_choices[1][0]
    include_empty = forms.BooleanField(label=_('Include empty'), required=False, initial=False)


class EstimateYearForm(forms.Form):
    frame_from_year = forms.IntegerField(label=_('From'), widget=forms.TextInput(
        attrs={'class': "short_field_white"}))
    frame_to_year = forms.IntegerField(label=_('To'), widget=forms.TextInput(
        attrs={'class': "short_field_white"}))