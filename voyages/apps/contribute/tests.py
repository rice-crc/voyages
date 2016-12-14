from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
import random
from django.contrib.auth.models import User
from imputed import *
from models import *
from forms import *
from voyages.apps.voyage.models import *
import numbers
import csv
import json

@override_settings(LANGUAGE_CODE='en')
class TestAuthentication(TestCase):
    """
    Test the basic login mechanism of the Admin site
    """

    fixtures = ['users.json']

    def create_random_user(self):
        """
        Create a user with the specified username and password
        Return the object, username and password
        """
        username = "test_user" + str(random.randint(0, 1000000))
        password = "test_user" + str(random.randint(0, 100000))

        tmpUser = User.objects.create(username=username)
        tmpUser.set_password(password)
        tmpUser.save()
        return tmpUser, username, password

    def test_invalid_login_info(self):
        """
        Attempt to login using an invalid username/password
        """
        # Should redirect
        response = self.client.post(reverse('contribute:index'),
                                    {'id_username': 'admin', 'id_password': 'should_not_work'}, follow=True)
        self.assertEqual(response.redirect_chain[0][0], '/accounts/login/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('account_login'),
                                    {'id_username': 'admin', 'id_password': 'should_not_work'})
        self.assertEqual(response.status_code, 200)
        # Should display the error message
        self.assertContains(response, "Your username/email and password didn't match. Please try again")

        # Should fail
        login_res = self.client.login(username='admin', password="random_pass")
        self.assertEqual(login_res, False)

        # Should redirect, since we are not logged in
        response = self.client.get(reverse('contribute:index'), follow=True)
        self.assertRedirects(response, reverse('account_login'), status_code=302, target_status_code=200)


    def test_valid_login_info(self):
        """
        Attempt to login using a valid combination of user name and password
        """
        # Create a user
        user_obj, usr_name, usr_password = self.create_random_user()

        # Perform login then check if we can access the user_index page
        login_res = self.client.login(username=usr_name, password=usr_password)
        self.assertEqual(login_res, True)
        response = self.client.get(reverse('contribute:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to the Contribute Section")
        # Not a staff user
        self.assertNotContains(response, "Live Admin")

        user_obj.is_staff=True
        user_obj.save()
        login_res = self.client.login(username=usr_name, password=usr_password)
        self.assertEqual(login_res, True)
        response = self.client.get(reverse('contribute:index'))
        self.assertEqual(response.status_code, 200)

        #Is a staff user
        self.assertContains(response, "Live Admin")


    def test_user_or_email(self):
        # using username with bad password
        result = self.client.login(username='testuser', password='xxxxxx')
        self.assertFalse(result)

        # using username with good password
        result = self.client.login(username='testuser', password='testuser')
        self.assertTrue(result)

        # using email with bad password
        result = self.client.login(username='test@user.com', password='xxxxxx')
        self.assertFalse(result)

        # using email with good password
        result = self.client.login(username='test@user.com', password='testuser')
        self.assertTrue(result)

class TestImputedDataCalculation(TestCase):
    """
    Here we test the converted SPSS script that should generate imputed variables
    """
    
    fixtures = ['geographical.json', 'shipattributes.json', 'groupings.json', 'outcomes.json']
    
    def parse_csv(self, file_name):            
        data = {}
        with open(file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row = {k: v if v and v.strip() != '' else None for k, v in row.items()}
                data[row['voyageid']] = row
        return data
    
    def test_dataset(self):
        import os
        folder = os.path.dirname(os.path.realpath(__file__)) + '/testdata/'
        errors = self.compute_imputed_csv(folder + 'ImputeTestData.csv', folder + 'ImputeTestDataOutput.csv')        
        if len(errors) > 0:
            print 'Failed count ' + str(len(errors))
        self.assertEqual(0, len(errors), '\n'.join(errors.values()))
    
    def compute_imputed_csv(self, input_csv, output_csv, dump_file=None):
        # The test dataset is divided into two CSV files, one contains the source
        # variable data and the other contains the expected output.
        test_input = self.parse_csv(input_csv)
        test_output = self.parse_csv(output_csv)
        if len(test_input) != len(test_output):
            raise Exception('Input and output files do not have the same row count')
        
        # Join input and output data
        for k, v in test_input.items():
            v.update(test_output[k])
        errors = {}
        
        def is_number(s):
            try:
                float(s)
                return True
            except:
                return False
        
        def mismatch_text(m):
            return m[0] + ': expected "' + str(m[1]) + '" [' + str(type(m[1])) + '], got "' + str(m[2]) + '" [' + str(type(m[2])) + '] instead'
        
        def str_dict(d):
            return '{\n' + ',\n'.join(['\t{0}: {1} [{2}]'.format(k, v, type(v)) for k, v in sorted(d.items()) if not k.startswith('_')]) + '\n}'
        
        computed_data = []
        first = True
        for voyage_id, row in test_input.items():
            interim = self.interim_voyage(row)
            try:
                all_vars = compute_imputed_vars(interim)[2]
            except Exception as ex:
                errors[voyage_id] = 'Exception raised: ' + str(ex)
                continue 
            # Check that the imputed fields all match.
            mismatches = []
            for k, v in all_vars.items():
                if not k in row:
                    if first:
                        print "WARNING: Missing field in target output: " + k
                    continue
                expected = row[k]
                if is_number(v) or is_number(expected):
                    expected = float(expected) if expected is not None else 0.0
                    v = float(v) if v is not None else 0.0
                    if abs(v - expected) >= 0.01:
                        mismatches.append((k, expected, v))
                elif v != expected:
                    mismatches.append((k, expected, v))
            all_vars['voyageid'] = voyage_id
            computed_data.append(all_vars)
            if len(mismatches) > 0:
                mismatches = sorted(mismatches, key=lambda m: m[0])
                errors[voyage_id] = 'Mismatches on voyage id ' + voyage_id + ':\n' + \
                    ',\n'.join(['\t' + mismatch_text(m) for m in mismatches]) + \
                    '\nInterim numbers:\n' + str_dict({sn.var_name: sn.number for sn in interim.slave_numbers.all()}) + \
                    '\nInterim:\n' + str_dict(vars(interim)) + \
                    '\nAll variables:\n' + str_dict(all_vars)
            first = False
            interim.delete()
        
        if dump_file is not None and len(computed_data) > 0:
            with open(dump_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, computed_data[0].keys())
                writer.writeheader()
                for row in computed_data:
                    writer.writerow(row)
        
        return errors
        
    def interim_voyage(self, dict):
        # TODO: this code may be placed somewhere else so that
        # it can be reused.
        nat_from_value = fn_from_value(Nationality)
        place_from_value = fn_from_value(Place)
        rig_from_value = fn_from_value(RigOfVessel)
        tontype_from_value = fn_from_value(TonType)
        outcome_from_value = fn_from_value(ParticularOutcome)
        resistance_from_value = fn_from_value(Resistance)
        
        def date_from_triple(m, d, y):
            arr = [dict[m], dict[d], dict[y]]
            arr = [str(x) if x else '' for x in arr]
            result = ','.join(arr)
            return result if result != ',,' else None
        
        interim = InterimVoyage()
        interim.name_of_vessel = dict['shipname']
        interim.year_ship_constructed = dict['yrcons']
        interim.year_ship_registered = dict['yrreg']
        interim.ship_construction_place = place_from_value(dict['placcons'])
        interim.ship_registration_place = place_from_value(dict['placreg'])
        interim.national_carrier = nat_from_value(dict['national'])
        interim.rig_of_vessel = rig_from_value(dict['rig'])
        interim.tonnage_of_vessel = dict['tonnage']
        interim.ton_type = tontype_from_value(dict['tontype'])
        interim.guns_mounted = dict['guns']
        interim.first_ship_owner = dict['ownera']
        interim.second_ship_owner = dict['ownerb']
        # interim.additional_ship_owners = dict['ownerc' d, e, f...]
        interim.voyage_outcome = outcome_from_value(dict['fate'])
        interim.african_resistance = resistance_from_value(dict['resistance'])
        interim.first_port_intended_embarkation = place_from_value(dict['embport'])
        interim.second_port_intended_embarkation = place_from_value(dict['embport2'])
        interim.first_port_intended_disembarkation = place_from_value(dict['arrport'])
        interim.second_port_intended_disembarkation = place_from_value(dict['arrport2'])
        interim.port_of_departure = place_from_value(dict['portdep'])        
        interim.number_of_ports_called_prior_to_slave_purchase = dict['nppretra']
        interim.first_place_of_slave_purchase = place_from_value(dict['plac1tra'])
        interim.second_place_of_slave_purchase = place_from_value(dict['plac2tra'])
        interim.third_place_of_slave_purchase = place_from_value(dict['plac3tra'])
        interim.principal_place_of_slave_purchase = place_from_value(dict['majbuypt'])
        interim.place_of_call_before_atlantic_crossing = place_from_value(dict['npafttra'])
        interim.number_of_new_world_ports_called_prior_to_disembarkation = dict['nppretra']
        interim.first_place_of_landing = place_from_value(dict['sla1port'])
        interim.second_place_of_landing = place_from_value(dict['adpsale1'])
        interim.third_place_of_landing = place_from_value(dict['adpsale2'])
        interim.principal_place_of_slave_disembarkation = place_from_value(dict['majselpt'])
        interim.port_voyage_ended = place_from_value(dict['portret'])
        interim.date_departure = date_from_triple('datedepb', 'datedepa', 'datedepc')
        interim.date_slave_purchase_began = date_from_triple('d1slatrb', 'd1slatra', 'd1slatrc')
        interim.date_vessel_left_last_slaving_port = date_from_triple('dlslatrb', 'dlslatra', 'dlslatrc')
        interim.date_first_slave_disembarkation = date_from_triple('datarr33', 'datarr32', 'datarr34')
        interim.date_second_slave_disembarkation = date_from_triple('datarr37', 'datarr36', 'datarr38')
        interim.date_third_slave_disembarkation = date_from_triple('datarr40', 'datarr39', 'datarr41')
        interim.date_return_departure = date_from_triple('ddepamb', 'ddepam', 'ddepamc')
        interim.date_voyage_completed = date_from_triple('datarr44', 'datarr43', 'datarr45')
        interim.length_of_middle_passage = dict['voyage']
        interim.first_captain = dict['captaina']
        interim.second_captain = dict['captainb']
        interim.third_captain = dict['captainc']
        interim.save()
        number_variables = ['ncar13', 'ncar15', 'ncar17', 'tslavesd', 
            'tslavesp', 'slas32', 'slas36', 'slas39', 'slaarriv', 'sladvoy',
            'men1', 'men4', 'men5', 'women1', 'women4', 'women5', 'adult1',
            'adult4', 'adult5', 'girl1', 'girl4', 'girl5', 'boy1', 'boy4',
            'boy5', 'child1', 'child4', 'child5', 'infant1', 'infant4',
            'male1', 'male4', 'male5', 'female1', 'female4', 'female5',
            'men3', 'men6', 'women3', 'women6', 'adult3', 'adult6', 'girl3',
            'girl6', 'boy3', 'boy6', 'child3', 'child6', 'infant3', 'male3',
            'male6', 'female3', 'female6', 'men2', 'women2', 'adult2',
            'girl2', 'boy2', 'child2', 'male2', 'female2']
        numbers_added = {}
        for var_name in number_variables:
            var_value = dict.get(var_name)
            if var_value is None:
                continue
            number = InterimSlaveNumber()
            number.interim_voyage = interim
            number.var_name = var_name.upper()
            number.number = var_value
            number.save()
            numbers_added[number.var_name] = number
        return interim

class TestEditorialPlatform(TestCase):
    """
    Here we will test the editorial platform by creating mock
    user contributions and following possible editorial workflows
    until their conclusion (e.g. publication).
    """
    
    fixtures = ['geographical.json', 'shipattributes.json', 'groupings.json', 'outcomes.json']
    
    def test_workflow(self):
    
        # Create a user for the contributor.
        the_password = 'mypass'
        contributor = User.objects.create_user(username='contributor', password=the_password)
        
        # Create a reviewer user
        reviewer = User.objects.create_user(username='reviewer', password=the_password)
        
        # Create an editor user
        editor = User.objects.create_superuser('editor', 'editor@voyages.org', the_password)
        
        def login(user):
            return self.client.login(username=user.username, password=the_password)
            
        self.assertTrue(login(contributor))
        response = self.client.get(reverse('contribute:new_voyage'), follow=True)
        self.assertEqual(response.status_code, 200)
        data = response.context
        contribution = data['contribution']
        interim = data['interim']
        form = data['form']
        numbers = data['numbers']
        self.assertNotEqual(contribution, None)
        self.assertNotEqual(interim, None)
        self.assertNotEqual(form, None)
        self.assertEqual(numbers, {})
        
        # Check that the fields are blank (just a sample, there are too many to check).
        self.assertEqual(interim.name_of_vessel, None)
        self.assertEqual(interim.date_departure, None)
        
        # Fill out form and submit contribution.
        interim.name_of_vessel = u'Lion'
        interim.year_ship_constructed = 1642
        interim.year_ship_registered = 1645
        interim.ship_construction_place = Place.objects.get(place='London')
        interim.ship_registration_place = interim.ship_construction_place
        interim.national_carrier = Nationality.objects.get(label='Great Britain')
        # Many other fields.
        from django.forms import model_to_dict
        form = InterimVoyageForm(model_to_dict(interim), instance=interim)
        is_valid = form.is_valid()
        if not is_valid:
            # Avoid calling form.errors if not needed.
            self.assertTrue(is_valid, form.errors.as_text())
        
        # Slave numbers.
        prefix = 'interim_slave_number_'
        slave_numbers = {
            u'interim_slave_number_CREW1': 25,
            u'interim_slave_number_CREW2': 19,
            u'interim_slave_number_CREW3': 17,
            u'interim_slave_number_CREW4': 12,
            u'interim_slave_number_CREW5': 11,
            u'interim_slave_number_SAILD1': 2,
            u'interim_slave_number_SAILD2': 5,
            u'interim_slave_number_SAILD3': 2,
            u'interim_slave_number_SAILD4': 2,
            u'interim_slave_number_SAILD5': 1,
            u'interim_slave_number_DIED': 10,
        }
        
        # Submit data to save record (no source references yet).
        ajax_data = {k: v.pk if hasattr(v, 'pk') else v for k, v in form.cleaned_data.items() if v is not None}
        ajax_data.update(slave_numbers)
        json_response = self.client.post(
            reverse('contribute:interim_save_ajax', kwargs={'contribution_type': 'new', 'contribution_id': contribution.pk}),
            ajax_data)
        parsed_response = json.loads(json_response.content)
        self.assertTrue(parsed_response['valid'], json_response.content)
        self.assertEqual(len(parsed_response['errors']), 0, json_response.content)
        
        # Create a few user contributions
        #NewVoyageContribution()
        #EditVoyageContribution()
        #MergeVoyagesContribution()
        #DeleteVoyageContribution()
        # response = self.client.post(reverse('begin_editorial_review'), {'contribution_id': 'aaaa'})
        # response = self.client.post(
        #     reverse('submit_editorial_decision', kwargs={'editor_contribution_id': 0}),
        #     {'editorial_decision': 'aaaa', 'decision_message': 'bbbb', 'created_voyage_id': None})
        # response = self.client.post(reverse('begin_editorial_review'), {'contribution_id': 'aaaa'})
        # response = self.client.post(reverse('begin_editorial_review'), {'contribution_id': 'aaaa'})
        