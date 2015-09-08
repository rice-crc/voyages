from django import forms
from django.contrib.auth.forms import AuthenticationForm
from voyages.apps.contribute.models import *
from voyages.extratools import AdvancedEditor
from django.utils.translation import ugettext_lazy as __

class AdminFaqAdminForm(forms.ModelForm):
    """
    Form for editing HTML for Admin FAQ
    """
    question = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':60}))
    answer = forms.CharField(widget=AdvancedEditor(attrs={'class' : 'tinymcetextarea', 'label': 'Answer'}))

    class Meta:
        model = AdminFaq

class LoginForm(AuthenticationForm):
    x = 1

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _("Username or Email")