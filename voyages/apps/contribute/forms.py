# Create your models here.
from django import forms

class DownloadFileForm(forms.Form):
    downloadfile = forms.FileField(label='Select your file')
    filetitle = forms.CharField(max_length=50)
