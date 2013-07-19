from django import forms
import autocomplete_light
from .models import *
from django.forms import widgets
from django.forms.extras.widgets import *
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
    short_ref = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':60}))
    full_ref = forms.CharField(widget=AdvancedEditor(attrs={'class' : 'tinymcetextarea'}))

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
    threshold = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': "medium_field"}))
    lower_bound = forms.IntegerField(widget=forms.TextInput(attrs={'class': "short_field"}))
    upper_bound = forms.IntegerField(widget=forms.TextInput(attrs={'class': "short_field"}))


class SimpleSelectSearchForm(forms.Form):
    """
    Simple checkbox search form
    """
    CHOICES = ["Random",]
    def __init__(self, listChoices, *args, **kwargs):
        CHOICES = listChoices
        super(SimpleSelectSearchForm, self).__init__(*args, **kwargs)

    selects = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICES)