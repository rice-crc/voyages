from django import forms
from voyages.apps.help.models import *
from voyages.extratools import AdvancedEditor

class FaqAdminForm(forms.ModelForm):
    """
    Form for editing HTML for FAQ answer
    """
    question = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':60}))
    answer = forms.CharField(widget=AdvancedEditor(attrs={'class' : 'tinymcetextarea'}))
    question_order = forms.IntegerField()

    class Meta:
        model = Faq

