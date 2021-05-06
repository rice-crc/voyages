from __future__ import unicode_literals

from collections import OrderedDict

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField

from voyages.apps.contribute.models import AdminFaq, InterimVoyage, UserProfile
from voyages.apps.voyage.models import Voyage
from voyages.extratools import AdvancedEditor

legal_terms_title = _('Terms and Conditions')
legal_terms_paragraph = _("""I warrant that I have the right to contribute the
                          following data to the Voyages  Database and its
                          inclusion in the Voyages Database will not infringe
                          anyone\'s  intellectual property rights. I also agree
                          that this data will become part of  the Voyages: The
                          Trans-Atlantic Slave Trade Database website and will
                          be  governed by any applicable licenses.""")


class AdminFaqAdminForm(forms.ModelForm):
    """
    Form for editing HTML for Admin FAQ
    """
    question = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4,
        'cols': 60
    }))
    answer = forms.CharField(widget=AdvancedEditor(attrs={
        'class': 'tinymcetextarea',
        'label': 'Answer'
    }))

    class Meta:
        model = AdminFaq
        fields = '__all__'


class LoginForm(AuthenticationForm):
    x = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _("Username or Email")


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('First name'))
    last_name = forms.CharField(max_length=30, label=_('Last name'))
    institution = forms.CharField(
        max_length=255, label=_('Institution'), required=False)
    new_material_and_sources = forms.CharField(
        max_length=1000,
        label=_('Brief description of new material and sources'),
        required=False)
    terms = forms.CharField(widget=forms.Textarea,
                            required=False,
                            label=legal_terms_title,
                            initial=legal_terms_paragraph)
    agree_to_terms = forms.BooleanField(required=True, label=_(
        'Agree to the terms and conditions above'))
    captcha = CaptchaField()

    # This init method will reorder the fields so that
    # the form is presented just the way we want
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        self.fields = OrderedDict(
            sorted(list(self.fields.items()),
                   key=lambda k: key_order.index(k[0])
                   if k[0] in key_order else 1000))
        self.fields['terms'].widget.attrs['readonly'] = True

    def signup(self, _, user):
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
        profile.new_material_and_sources = self.cleaned_data[
            'new_material_and_sources']
        profile.save()


class ContributionVoyageSelectionForm(forms.Form):
    """
    A class for contribution forms that select one or
    more voyage ids.
    """

    def __init__(self,
                 *args,
                 data=None,
                 min_selection=1,
                 max_selection=None,
                 **kwargs):
        super().__init__(data, *args, **kwargs)
        self.min_selection = min_selection
        self.max_selection = max_selection
        self.selected_voyages = []
        self.ids = forms.CharField(max_length=255, required=True)

    def clean_ids(self):
        data = self.cleaned_data['ids']
        self.selected_voyages = []
        # Ensure that the CSV string data only contains voyage_ids
        # that are current present in the database.
        try:
            ids = [int(x) for x in data.split(',')]
        except Exception:
            raise forms.ValidationError(_('Improperly formatted field'))
        self.selected_voyages = ids
        id_count = len(ids)
        if id_count < self.min_selection:
            raise forms.ValidationError(
                _('At least %d voyage(s) should be '
                  'provided') % self.min_selection)
        if self.max_selection is not None and id_count > self.max_selection:
            raise forms.ValidationError(
                _('At most %d voyage(s) should be '
                  'provided') % self.max_selection)
        matches = Voyage.all_dataset_objects.filter(voyage_id__in=ids).count()
        if matches != id_count:
            raise forms.ValidationError(
                _('Some of the provided voyage_ids are invalid'))
        return ids


default_name_help_text = _('Enter last name , first name.')


class InterimVoyageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleaned_data = {}

    def full_clean(self):
        self.cleaned_data = {}
        super().full_clean()
        for k, _ in list(self._errors.items()):
            if k.startswith('date_'):
                del self._errors[k]
        return self.cleaned_data

    class Meta:
        model = InterimVoyage
        fields = '__all__'
        help_texts = {
            'national_carrier': _('If not country of registration, use '
                                  'the comments box to explain coding.'),
            'first_ship_owner': default_name_help_text,
            'second_ship_owner': default_name_help_text,
            'additional_ship_owners': default_name_help_text,
            'first_captain': default_name_help_text,
            'second_captain': default_name_help_text,
            'additional_captain': default_name_help_text,
            'principal_place_of_slave_purchase':
            _('If more than one place of purchase, use the comments box to '
              'explain choice of principal place.'),
            'principal_place_of_slave_disembarkation':
            _('If more than one place of landing, use the comments box to '
              'explain choice of principal place.'),
        }
        labels = {
            # Ship, nation, owners
            'name_of_vessel': _('Name of vessel'),
            'year_ship_constructed': _('Year of ship construction'),
            'year_ship_registered': _('Year of ship registration'),
            'ship_construction_place': _('Place where ship constructed'),
            'ship_registration_place': _('Place where ship registered'),
            'national_carrier': _('National carrier'),
            'rig_of_vessel': _('Rig of vessel'),
            'tonnage_of_vessel': _('Tonnage of vessel'),
            'ton_type': _('Definition of ton'),
            'guns_mounted': _('Guns mounted'),
            'first_ship_owner': _('First or managing owner of venture'),
            'second_ship_owner': _('Second owner of venture'),
            'additional_ship_owners': _('Other owners'),
            # Outcome
            'voyage_outcome': _('Outcome of voyage'),
            'african_resistance': _('African resistance'),
            # Itinerary
            'first_port_intended_embarkation':
            _('First port of intended embarkation'),
            'second_port_intended_embarkation':
            _('Second port of intended embarkation'),
            'first_port_intended_disembarkation':
            _('First port of intended disembarkation'),
            'second_port_intended_disembarkation':
            _('Second port of intended disembarkation'),
            'port_of_departure': _('Port of departure'),
            'number_of_ports_called_prior_to_slave_purchase':
            _('Number of ports called prior to slave purchase'),
            'first_place_of_slave_purchase':
            _('First place of slave purchase'),
            'second_place_of_slave_purchase':
            _('Second place of slave purchase'),
            'third_place_of_slave_purchase':
            _('Third place of slave purchase'),
            'principal_place_of_slave_purchase':
            _('Principal place of slave purchase'),
            'place_of_call_before_atlantic_crossing':
            _('Places of call before Atlantic crossing'),
            'number_of_new_world_ports_called_prior_to_disembarkation':
            _('Number of New World ports of call before disembarkation'),
            'first_place_of_landing': _('First place of landing'),
            'second_place_of_landing': _('Second place of landing'),
            'third_place_of_landing': _('Third place of landing'),
            'principal_place_of_slave_disembarkation':
            _('Principal place of slave disembarkation'),
            'port_voyage_ended': _('Port at which voyage ended'),
            # Dates
            'date_departure': _('Date of departure'),
            'date_slave_purchase_began': _('Date that slave purchase began'),
            'date_vessel_left_last_slaving_port':
            _('Date that vessel left last slaving port'),
            'date_first_slave_disembarkation':
            _('Date of first disembarkation of slaves'),
            'date_second_slave_disembarkation':
            _('Date of second disembarkation of slaves'),
            'date_third_slave_disembarkation':
            _('Date of third disembarkation of slaves'),
            'date_return_departure': _('Date that ship left on return voyage'),
            'date_voyage_completed': _('Date when voyage completed'),
            'length_of_middle_passage': _('Length of Middle Passage in days'),
            # Captains
            'first_captain': _('First captain of voyage'),
            'second_captain': _('Second captain of voyage'),
            'third_captain': _('Third captain of voyage')
        }
