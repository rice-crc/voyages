from django import forms
from voyages.apps.contribute.models import *
from voyages.extratools import AdvancedEditor

class AdminFaqAdminForm(forms.ModelForm):
    """
    Form for editing HTML for Admin FAQ
    """
    question = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':60}))
    answer = forms.CharField(widget=AdvancedEditor(attrs={'class' : 'tinymcetextarea', 'label': 'Answer'}))

    class Meta:
        model = AdminFaq

