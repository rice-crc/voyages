from django import forms
import autocomplete_light
from .models import *
from voyages.extratools import AdvancedEditor



class UploadFileForm(forms.Form):
    """Form to uploading files in download section"""
    downloadfile = forms.FileField(label='Select your file')


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


class SimpleTextForm(forms.Form):
    """
    Simple one field form to perform text search
    """
    text_search = forms.CharField(widget=forms.TextInput(attrs={'class': "query-builder-text"}))


class SimpleNumericSearchForm(forms.Form):
    """
    Simple numeric search form
    """
    OPERATORS = (('1', 'Between'), ('2', 'At most'), ('3', 'At least'), ('4', 'Is equal to'))
    options = forms.ChoiceField(choices=OPERATORS,
                                widget=forms.Select(attrs={'class': "select_field newly_inserted"}))
    threshold = forms.IntegerField(required=False, widget=forms.TextInput(
        attrs={'class': "medium_field"}))
    lower_bound = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': "short_field"}))
    upper_bound = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': "short_field"}))


class SimpleDateSearchForm(forms.Form):
    """
    Simple date search form
    """
    OPERATORS = (('1', 'Between'), ('2', 'Before'), ('3', 'After'), ('4', 'In'))
    options = forms.ChoiceField(choices=OPERATORS,
                                widget=forms.Select(attrs={'class': "date_field newly_inserted"}))
    from_month = forms.IntegerField(required=False, initial="01", widget=forms.TextInput(
        attrs={'class': "date_field_short", 'size': '2', 'maxlength': '2'}))
    from_year = forms.IntegerField(required=False, widget=forms.TextInput(
        attrs={'class': "date_field_long", 'size': '4', 'maxlength': '4'}))
    to_month = forms.IntegerField(required=False, initial="12", widget=forms.TextInput(
        attrs={'class': "date_field_short", 'size': '2', 'maxlength': '2'}))
    to_year = forms.IntegerField(required=False, widget=forms.TextInput(
        attrs={'class': "date_field_long", 'size': '4', 'maxlength': '4'}))

    threshold_month = forms.IntegerField(required=False, initial="MM", widget=forms.TextInput(
        attrs={'class': "date_field_short", 'size': '2', 'maxlength': '2'}))
    threshold_year = forms.IntegerField(required=False, initial="YYYY",widget=forms.TextInput(
        attrs={'class': "date_field_long", 'size': '4', 'maxlength': '4'}))


class SimpleSelectSearchForm(forms.Form):
    """
    Simple checkbox search form
    """
    INIT_CHOICES = (('1', 'Yes'), ('2', 'No'))
    choice_field = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': 'var-checkbox'})
                    , choices=INIT_CHOICES)

    def __init__(self, listChoices, *args, **kwargs):
        super(SimpleSelectSearchForm, self).__init__(*args, **kwargs)
        self.fields['choice_field'].choices = listChoices


class SimpleSelectBooleanForm(forms.Form):
    BOOLEAN_CHOICES = (('1', 'Yes'), ('2', 'No'))

    choice_field = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'var-checkbox'}),
        choices=BOOLEAN_CHOICES)


class TimeFrameSpanSearchForm(forms.Form):
    frame_from_year = forms.IntegerField(label="From", widget=forms.TextInput(
        attrs={'class': "short_field_white"}))
    frame_to_year = forms.IntegerField(label = "To", widget=forms.TextInput(
        attrs={'class': "short_field_white"}))