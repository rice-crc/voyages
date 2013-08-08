from django import forms
from .models import *

class ImageAdminForm(forms.ModelForm):
    """
    Form for editing HTML for FAQ answer
    """
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':6, 'cols':60}))

    class Meta:
        model = Image
