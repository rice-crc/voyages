from django import forms
from .models import *

class ImageForm(forms.ModelForm):
    """
    Form for editing HTML for FAQ answer
    """
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 90}))

    class Meta:
        model = Image