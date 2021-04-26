from __future__ import unicode_literals

from django import forms

from .models import Image


class ImageAdminForm(forms.ModelForm):
    """
    Form for editing HTML for FAQ answer
    """
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 6,
        'cols': 60
    }))

    class Meta:
        model = Image
        fields = '__all__'


class ResultsPerPageOptionForm(forms.Form):
    choices = (('1', 10), ('2', 20), ('3', 50), ('4', 100), ('5', 200))
    option = forms.ChoiceField(
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'}),
        choices=choices,
        initial='2')

    def cleaned_option(self):
        try:
            option_value = self.cleaned_data['option']
        except Exception:
            option_value = '2'

        return dict(self.fields['option'].choices)[option_value]
