from django import forms
import autocomplete_light
from .models import *

class UploadFileForm(forms.Form):
    """Form to uploading files in download section"""
    downloadfile = forms.FileField(label='Select your file')


class VoyageCaptainConnectionForm(forms.ModelForm):
    """
    Form for Captain Connection (this is inline).
    """
    class Meta:
        model = VoyageCaptainConnection
        widgets = autocomplete_light.get_widgets_dict(VoyageCaptainConnection)


class VoyageShipForm(forms.ModelForm):
    """
    Form for Captain Connection (this is inline).
    """
    class Meta:
        model = VoyageShip
        widgets = autocomplete_light.get_widgets_dict(VoyageShip)


class VoyageShipOwnerConnectionForm(forms.ModelForm):
    """
    Form for Captain Connection (this is inline).
    """
    class Meta:
        model = VoyageShipOwnerConnection
        widgets = autocomplete_light.get_widgets_dict(VoyageShipOwnerConnection)