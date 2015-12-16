from captcha.fields import CaptchaField
from collections import OrderedDict
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from voyages.apps.contribute.models import *
from voyages.apps.voyage.models import Voyage
from voyages.extratools import AdvancedEditor

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
    terms = forms.CharField(widget=forms.Textarea, required=False, label=_('Terms and conditions'),
                            initial=_('All the legal stuff goes here'))
    agree_to_terms = forms.BooleanField(required=True, label=_('Agree to the terms and conditions above'))
    captcha = CaptchaField()

    # This init method will reorder the fields so that
    # the form is presented just the way we want
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        key_order = [
            'first_name',
            'last_name',
            'institution',
            'new_material_and_sources',
            'email',
            'password1',
            'password2',
            'captcha',
            'terms',
            'agree_to_terms',
        ]
        self.fields = OrderedDict(sorted(self.fields.items(), key=lambda k: key_order.index(k[0]) if k[0] in key_order else 1000))
        self.fields['terms'].widget.attrs['readonly'] = True

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if 'password1' in self.cleaned_data:
            user.set_password(self.cleaned_data['password1'])
            user.email = self.cleaned_data['email']
            user.username = user.email
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.institution = self.cleaned_data['institution']
        profile.new_material_and_sources = self.cleaned_data['new_material_and_sources']
        profile.save()

class DeleteContributionForm(forms.Form):
    """
    This form will gather a collection of voyage_id values that
    should be deleted according to this contribution.
    """
    delete_ids = forms.CharField(max_length=255, required=True)
    notes = forms.CharField(max_length=1000, required=True)

    def clean_delete_ids(self):
        data = self.cleaned_data['delete_ids']
        # Ensure that the CSV string data only contains voyage_ids
        # that are current present in the database.
        try:
            ids = [int(x) for x in data.split(',')]
        except:
            raise forms.ValidationError(_('Improperly formatted field'))
        id_count = len(ids)
        if id_count == 0:
            raise forms.ValidationError(_('At least one voyage_id should be provided'))
        matches = Voyage.objects.filter(voyage_id__in=ids).count()
        if matches != id_count:
            raise forms.ValidationError(_('Some of the provided voyage_ids is invalid'))
        return ids

