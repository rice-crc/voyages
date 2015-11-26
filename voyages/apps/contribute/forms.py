from django import forms
from django.contrib.auth.forms import AuthenticationForm
from voyages.apps.contribute.models import *
from voyages.extratools import AdvancedEditor
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField
from collections import OrderedDict

class AdminFaqAdminForm(forms.ModelForm):
    """
    Form for editing HTML for Admin FAQ
    """
    question = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':60}))
    answer = forms.CharField(widget=AdvancedEditor(attrs={'class' : 'tinymcetextarea', 'label': 'Answer'}))

    class Meta:
        model = AdminFaq
        fields = '__all__'

class LoginForm(AuthenticationForm):
    x = 1

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _("Username or Email")

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('First name'))
    last_name = forms.CharField(max_length=30, label=_('Last name'))
    institution = forms.CharField(max_length=255, label=_('Institution'), required=False)
    new_material_and_sources = forms.CharField(max_length=1000, label=_('Brief description of new material and sources'), required=False)

    captcha = CaptchaField()

    # This init method will reorder the fields so that
    # the form is presented just the way we want
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        key_order = [
            'first_name',
            'last_name',
            'email',
            'institution',
            'new_material_and_sources',
            'password1',
            'password2',
            'captcha'
        ]
        self.fields = OrderedDict(sorted(self.fields.items(), key=lambda k: key_order.index(k[0]) if k[0] in key_order else 1000))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        user.username = user.email
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.institution = self.cleaned_data['institution']
        profile.new_material_and_sources = self.cleaned_data['new_material_and_sources']
        profile.save()
