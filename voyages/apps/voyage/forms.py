from __future__ import absolute_import, unicode_literals

from builtins import map, str

from django import forms
from django.utils.translation import ugettext_lazy as u_
from autocomplete_light import shortcuts as autocomplete_light

from voyages.extratools import AdvancedEditor

from . import graphs
from .globals import (list_months, table_columns, table_functions,
                      table_rows, voyage_timeline_variables)
from .models import (VoyageCaptainConnection, VoyageCrew, VoyageDates,
                     VoyageItinerary, VoyageOutcome, VoyageShip,
                     VoyageShipOwnerConnection, VoyageSlavesNumbers,
                     VoyageSources, VoyageSourcesConnection)


class UploadFileForm(forms.Form):
    """Form to uploading files in download section"""
    downloadfile = forms.FileField(label=u_('Select your file'))


class VoyageBaseForm(forms.Form):
    # Use a char field to keep track of the order of shown forms. Hide it
    # because it is irrelavent to the user. If not shown use empty string, if
    # shown use a number, higher numbers will be shown further down. This is
    # used mostly if not solely in the javascript code

    is_shown_field = forms.CharField(
        required=False, widget=forms.HiddenInput())
    var_name_field = forms.CharField(required=True, widget=forms.HiddenInput())

    def is_form_shown(self):
        """
        Determines if form is used in building the query, and if it is shown on
        the page
        """
        return not not self.cleaned_data['is_shown_field']


# Voyage
# Ship, Nation, Owners


class VoyageShipForm(autocomplete_light.ModelForm):
    """
    Form for Voyage Ship (this is inline).
    """

    class Meta:
        model = VoyageShip
        fields = '__all__'


class VoyageShipOwnerConnectionForm(autocomplete_light.ModelForm):
    """
    Form for Ship Owner Outcome (this is inline).
    """

    class Meta:
        model = VoyageShipOwnerConnection
        fields = '__all__'


# Voyage Outcome
class VoyageOutcomeForm(autocomplete_light.ModelForm):
    """
    Form for Voyage Outcome (this is inline).
    """

    class Meta:
        model = VoyageOutcome
        fields = '__all__'


# Voyage Itinerary
class VoyageItineraryForm(autocomplete_light.ModelForm):
    """
    Form for Voyage Itinerary (this is inline).
    """

    class Meta:
        model = VoyageItinerary
        fields = '__all__'


# Voyage Dates
class VoyageDatesForm(autocomplete_light.ModelForm):
    """
    Form for Voyage Dates (this is inline).
    """

    class Meta:
        model = VoyageDates
        fields = '__all__'


# Voyage Captain and Crew
class VoyageCaptainConnectionForm(autocomplete_light.ModelForm):
    """
    Form for Captain Connection (this is inline).
    """

    class Meta:
        model = VoyageCaptainConnection
        fields = '__all__'


class VoyageCrewForm(autocomplete_light.ModelForm):
    """
    Form for Voyage Crew (this is inline).
    """

    class Meta:
        model = VoyageCrew
        fields = '__all__'


# Voyage Slaves (numbers + characteristics)
class VoyageSlavesNumbersForm(autocomplete_light.ModelForm):
    """
    Form for Voyage Characteristics (this is inline).
    """

    class Meta:
        model = VoyageSlavesNumbers
        fields = '__all__'
        exclude = ['percentage_adult', 'percentage_female']


# Voyage Sources
class VoyageSourcesConnectionForm(autocomplete_light.ModelForm):
    """
    Form for Voyage Characteristics (this is inline).
    """

    class Meta:
        model = VoyageSourcesConnection
        fields = '__all__'


class VoyagesSourcesAdminForm(forms.ModelForm):
    """
    Form for editing HTML for FAQ answer
    """
    short_ref = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4,
        'cols': 60
    }))
    full_ref = forms.CharField(widget=AdvancedEditor(
        attrs={'class': 'tinymcetextarea'}))

    class Meta:
        fields = '__all__'
        model = VoyageSources


class SimpleTextForm(VoyageBaseForm):
    """
    Simple one field form to perform text search
    """
    # TODO: Remove empty label
    text_search = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': "query-builder-text"}), label="")
    type_str = "plain_text"


class SimpleNumericSearchForm(VoyageBaseForm):
    """
    Simple numeric search form
    """
    type_str = "numeric"
    OPERATORS = (('1', u_('Between')), ('2', u_('At most')),
                 ('3', u_('At least')), ('4', u_('Is equal to')))
    options = forms.ChoiceField(
        choices=OPERATORS,
        widget=forms.Select(attrs={'class': "select_field newly_inserted"}))
    threshold = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={'class': "medium_field"}))
    lower_bound = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={'class': "short_field"}))
    upper_bound = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={'class': "short_field"}))


class SimpleDateSearchForm(VoyageBaseForm):
    """
    Simple date search form
    """
    type_str = "date"
    list_months = list_months
    OPERATORS = (('1', u_('Between')), ('2', u_('Before')),
                 ('3', u_('After')), ('4', u_('In')))
    options = forms.ChoiceField(
        choices=OPERATORS,
        widget=forms.Select(attrs={'class': "date_field newly_inserted"}))
    from_month = forms.CharField(
        required=False,
        initial="01",
        widget=forms.TextInput(attrs={
            'class': "date_field_short",
            'size': '2',
            'maxlength': '2'
        }))
    from_year = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': "date_field_long",
            'size': '4',
            'maxlength': '4'
        }))
    to_month = forms.CharField(
        required=False,
        initial="12",
        widget=forms.TextInput(attrs={
            'class': "date_field_short",
            'size': '2',
            'maxlength': '2'
        }))
    to_year = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': "date_field_long",
            'size': '4',
            'maxlength': '4'
        }))

    threshold_month = forms.CharField(
        required=False,
        initial="MM",
        widget=forms.TextInput(attrs={
            'class': "date_field_short",
            'size': '2',
            'maxlength': '2'
        }))
    threshold_year = forms.CharField(
        required=False,
        initial="YYYY",
        widget=forms.TextInput(attrs={
            'class': "date_field_long",
            'size': '4',
            'maxlength': '4'
        }))

    months = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        choices=list_months,
        initial=[x[0] for x in list_months])


class SimpleSelectSearchForm(VoyageBaseForm):
    """
    Simple checkbox search form
    """
    type_str = "select"
    choice_field = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'var-checkbox'}))


class SimplePlaceSearchForm(VoyageBaseForm):
    type_str = "select_three_layers"
    choice_field = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'var-checkbox'}))
    nested_choices = []


class SimpleSelectBooleanForm(VoyageBaseForm):
    BOOLEAN_CHOICES = (('1', u_('Yes')), ('2', u_('No')))
    type_str = "boolean"
    choice_field = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'var-checkbox'}),
        choices=BOOLEAN_CHOICES)


class TimeFrameSpanSearchForm(forms.Form):
    frame_from_year = forms.IntegerField(
        label=u_('From'),
        widget=forms.TextInput(
            attrs={'class': "short_field_white"}))
    frame_to_year = forms.IntegerField(
        label=u_('To'),
        widget=forms.TextInput(
            attrs={'class': "short_field_white"}))


class ResultsPerPageOptionForm(forms.Form):
    choices = (('1', 10), ('2', 15), ('3', 20), ('4', 30), ('5', 50),
               ('6', 100), ('7', 200))
    option = forms.ChoiceField(
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'}),
        choices=choices,
        initial='1')

    def cleaned_option(self):
        try:
            option_value = self.cleaned_data['option']
        except Exception:
            option_value = None

        if option_value is None:
            option_value = '1'

        return dict(self.fields['option'].choices)[option_value]


def extract(x):
    return (str(x[0]), x[1][0])


class TableSelectionForm(forms.Form):

    rowchoices = list(map(extract, enumerate(table_rows)))
    rows = forms.ChoiceField(label='Rows',
                             choices=rowchoices,
                             initial=[rowchoices[12][1]
                                      ])  # table_rows[12])
    rows.initial = [rowchoices[12][0]]
    colchoices = list(map(extract, enumerate(table_columns)))
    columns = forms.ChoiceField(label='Columns',
                                choices=colchoices,
                                initial=[colchoices[7][1]
                                         ])  # table_columns[1])
    columns.initial = [colchoices[1][0]]
    cellchoices = list(map(extract, enumerate(table_functions)))
    cells = forms.ChoiceField(label='Cells',
                              choices=cellchoices,
                              initial=[cellchoices[1][1]
                                       ])  # table_functions[1])
    cells.initial = [cellchoices[1][0]]
    omit_empty = forms.BooleanField(label='Omit empty',
                                    required=False,
                                    initial=True)


class GraphRemovePlotForm(forms.Form):
    # Creates a list of boolean fields for each tuple in the list,
    # (description, id)
    def __init__(self, lst, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for desc, i in lst:
            self.fields[str(i)] = forms.BooleanField(label=desc,
                                                     required=False,
                                                     initial=False)

    def get_to_del(self):
        result = []
        if self.is_valid():
            for i, _ in list(self.fields.items()):
                if self.cleaned_data[i]:
                    result.append(int(i))
        return result


class GraphSelectionForm(forms.Form):

    def __init__(self,
                 *args,
                 xfunctions=None,
                 xfield_label='X axis',
                 yfield_label='Y axis',
                 **kwargs):
        super().__init__(*args, **kwargs)

        def lmbd(x):
            return (str(x[0]), x[1].description)

        if xfunctions is None:
            xfunctions = graphs.other_graphs_x_axes
        self.xchoices = [lmbd(x) for x in enumerate(xfunctions)]
        self.ychoices = list(map(lmbd, enumerate(graphs.graphs_y_axes)))
        self.fields['xselect'] = forms.ChoiceField(
            label=u_(xfield_label), choices=self.xchoices)
        self.fields['yselect'] = forms.ChoiceField(
            label=u_(yfield_label), choices=self.ychoices)


class TimelineVariableForm(forms.Form):
    var_choices = [(v[0], v[1]) for v in voyage_timeline_variables]
    variable_select = forms.ChoiceField(
        label=u_('Timeline variable'),
        choices=var_choices, initial=var_choices[23])
