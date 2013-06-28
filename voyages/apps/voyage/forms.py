from django import forms
import autocomplete_light
from .models import *

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