from django import forms
import autocomplete_light
from .models import *
from voyages.extratools import AdvancedEditor
import globals

class UploadFileForm(forms.Form):
    """Form to uploading files in download section"""
    downloadfile = forms.FileField(label='Select your file')


    
class VoyageBaseForm(forms.Form):
    # Use a char field to keep track of the order of shown forms. Hide it because it is irrelavent to the user.
    # If not shown use empty string, if shown use a number, higher numbers will be shown further down.
    # This is used mostly if not solely in the javascript code
    
    is_shown_field = forms.CharField(required=False, widget=forms.HiddenInput())
    var_name_field = forms.CharField(required=True, widget=forms.HiddenInput())

    def is_form_shown(self):
        """
        Determines if form is used in building the query, and if it is shown on the page
        """
        #print dir(self)
        #print self
        return not not self.cleaned_data['is_shown_field']

# Voyage
# Ship, Nation, Owners
class VoyageShipForm(forms.ModelForm):
    """
    Form for Voyage Ship (this is inline).
    """
    class Meta:
        model = VoyageShip
        widgets = autocomplete_light.get_widgets_dict(VoyageShip)


class VoyageShipOwnerConnectionForm(forms.ModelForm):
    """
    Form for Ship Owner Outcome (this is inline).
    """
    class Meta:
        model = VoyageShipOwnerConnection
        widgets = autocomplete_light.get_widgets_dict(VoyageShipOwnerConnection)


# Voyage Outcome
class VoyageOutcomeForm(forms.ModelForm):
    """
    Form for Voyage Outcome (this is inline).
    """
    class Meta:
        model = VoyageOutcome
        widgets = autocomplete_light.get_widgets_dict(VoyageOutcome)


# Voyage Itinerary
class VoyageItineraryForm(forms.ModelForm):
    """
    Form for Voyage Itinerary (this is inline).
    """
    class Meta:
        model = VoyageItinerary
        widgets = autocomplete_light.get_widgets_dict(VoyageItinerary)


# Voyage Dates
class VoyageDatesForm(forms.ModelForm):
    """
    Form for Voyage Dates (this is inline).
    """
    class Meta:
        model = VoyageDates
        widgets = autocomplete_light.get_widgets_dict(VoyageDates)


# Voyage Captain and Crew
class VoyageCaptainConnectionForm(forms.ModelForm):
    """
    Form for Captain Connection (this is inline).
    """
    class Meta:
        model = VoyageCaptainConnection
        widgets = autocomplete_light.get_widgets_dict(VoyageCaptainConnection)


class VoyageCrewForm(forms.ModelForm):
    """
    Form for Voyage Crew (this is inline).
    """
    class Meta:
        model = VoyageCrew
        widgets = autocomplete_light.get_widgets_dict(VoyageCrew)


# Voyage Slaves (numbers + characteristics)
class VoyageSlavesNumbersForm(forms.ModelForm):
    """
    Form for Voyage Characteristics (this is inline).
    """
    class Meta:
        model = VoyageSlavesNumbers
        widgets = autocomplete_light.get_widgets_dict(VoyageSlavesNumbers)


# Voyage Sources
class VoyageSourcesConnectionForm(forms.ModelForm):
    """
    Form for Voyage Characteristics (this is inline).
    """
    class Meta:
        model = VoyageSourcesConnection
        widgets = autocomplete_light.get_widgets_dict(VoyageSourcesConnection)


class VoyagesSourcesAdminForm(forms.ModelForm):
    """
    Form for editing HTML for FAQ answer
    """
    short_ref = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 60}))
    full_ref = forms.CharField(widget=AdvancedEditor(attrs={'class': 'tinymcetextarea'}))

    class Meta:
        model = VoyageSources


class SimpleTextForm(VoyageBaseForm):
    """
    Simple one field form to perform text search
    """
    # TODO: Remove empty label
    text_search = forms.CharField(widget=forms.TextInput(attrs={'class': "query-builder-text"}), label="")
    type_str = "plain_text"


class SimpleNumericSearchForm(VoyageBaseForm):
    """
    Simple numeric search form
    """
    type_str = "numeric"
    OPERATORS = (('1', 'Between'), ('2', 'At most'), ('3', 'At least'), ('4', 'Is equal to'))
    options = forms.ChoiceField(choices=OPERATORS,
                                widget=forms.Select(attrs={'class': "select_field newly_inserted"}))
    threshold = forms.IntegerField(required=False, widget=forms.TextInput(
        attrs={'class': "medium_field"}))
    lower_bound = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': "short_field"}))
    upper_bound = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': "short_field"}))


class SimpleDateSearchForm(VoyageBaseForm):
    """
    Simple date search form
    """
    type_str = "date"
    list_months = globals.list_months
    OPERATORS = (('1', 'Between'), ('2', 'Before'), ('3', 'After'), ('4', 'In'))
    options = forms.ChoiceField(choices=OPERATORS,
                                widget=forms.Select(attrs={'class': "date_field newly_inserted"}))
    from_month = forms.CharField(required=False, initial="01", widget=forms.TextInput(
        attrs={'class': "date_field_short", 'size': '2', 'maxlength': '2'}))
    from_year = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': "date_field_long", 'size': '4', 'maxlength': '4'}))
    to_month = forms.CharField(required=False, initial="12", widget=forms.TextInput(
        attrs={'class': "date_field_short", 'size': '2', 'maxlength': '2'}))
    to_year = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': "date_field_long", 'size': '4', 'maxlength': '4'}))

    threshold_month = forms.CharField(required=False, initial="MM", widget=forms.TextInput(
        attrs={'class': "date_field_short", 'size': '2', 'maxlength': '2'}))
    threshold_year = forms.CharField(required=False, initial="YYYY",widget=forms.TextInput(
        attrs={'class': "date_field_long", 'size': '4', 'maxlength': '4'}))

    months = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=globals.list_months, initial=map(lambda x: x[0], globals.list_months))


class SimpleSelectSearchForm(VoyageBaseForm):
    """
    Simple checkbox search form
    """
    type_str = "select"
    choice_field = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': 'var-checkbox'}))

class SimplePlaceSearchForm(VoyageBaseForm):
    type_str = "select_three_layers"
    choice_field = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': 'var-checkbox'}))
    nested_choices = []

class SimpleSelectBooleanForm(VoyageBaseForm):
    BOOLEAN_CHOICES = (('1', 'Yes'), ('2', 'No'))
    type_str = "boolean"
    choice_field = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'var-checkbox'}),
        choices=BOOLEAN_CHOICES)

class TimeFrameSpanSearchForm(forms.Form):
    frame_from_year = forms.IntegerField(label="From", widget=forms.TextInput(
        attrs={'class': "short_field_white"}))
    frame_to_year = forms.IntegerField(label="To", widget=forms.TextInput(
        attrs={'class': "short_field_white"}))


class ResultsPerPageOptionForm(forms.Form):
    choices = (('1', 10), ('2', 15), ('3', 20), ('4', 30), ('5', 50), ('6', 100), ('7', 200))
    option = forms.ChoiceField(widget=forms.Select(attrs={'onchange': 'this.form.submit();'}), choices=choices, initial='1')

    def cleaned_option(self):
        try:
            option_value = self.cleaned_data['option']
        except:
            option_value = None

        if option_value is None:
            option_value = '1'

        return dict(self.fields['option'].choices)[option_value]

class TableSelectionForm(forms.Form):
    lmbd = lambda x: (str(x[0]), x[1][0])
    rowchoices = map(lmbd, enumerate(globals.table_rows))
    rows = forms.ChoiceField(label='Rows', choices=rowchoices, initial=[rowchoices[12][1]])#globals.table_rows[12])
    rows.initial = [rowchoices[12][0]]
    colchoices = map(lmbd, enumerate(globals.table_columns))
    columns = forms.ChoiceField(label='Columns', choices=colchoices, initial=[colchoices[1][1]])#globals.table_columns[1])
    columns.initial = [colchoices[1][0]]
    cellchoices = map(lmbd, enumerate(globals.table_functions))
    cells = forms.ChoiceField(label='Cells', choices=cellchoices, initial=[cellchoices[1][1]])#globals.table_functions[1])
    cells.initial = [cellchoices[1][0]]
    omit_empty = forms.BooleanField(label='Omit empty', required=False, initial=False)
    
