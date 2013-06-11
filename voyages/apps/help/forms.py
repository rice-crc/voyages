from django import forms
from django.db.models import get_model
from django.contrib.auth.models import User
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

class GlossarySearchForm(forms.ModelForm):
    """Form serves search in Glossary section
    """
    search_field = forms.CharField(label="")

    class Meta:
        model = Glossary
        fields = ['search_field']

from haystack.forms import HighlightedSearchForm

class FaqSearchForm(HighlightedSearchForm):
    """
    Use to search terms in FAQ section
    """
    #q = forms.CharField(required=True)
    #search_field = forms.CharField(label="")
    
    def search(self):
        sqs = super(HighlightedSearchForm)
        return sqs