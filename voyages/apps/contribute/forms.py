# Create your models here.
from django import forms

class UserFileForm(forms.Form):
    userfile = forms.FileField(label='Select your file', help_text='max. 2 MB?')
    filetitle = forms.CharField(max_length=50)