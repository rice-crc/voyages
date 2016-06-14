from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
import random
from django.contrib.auth.models import User
from imputed import *
from models import *
from voyages.apps.voyage.models import *
import numbers

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
        self.assertEqual(response.redirect_chain[0][0], 'http://testserver/accounts/login/')
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
    
    def test_dataset(self):
        # The test dataset is divided into two CSV files, one contains the source
        # variable data and the other contains the expected output.
        import csv
        import os
        folder = os.path.dirname(os.path.realpath(__file__))
        def parse_csv(file_name):            
            data = {}
            with open(folder + '/testdata/' + file_name) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row = {k: v if v and v.strip() != '' else None for k, v in row.items()}
                    data[row['voyageid']] = row
            return data
        
        test_input = parse_csv('ImputeTestData.csv')
        test_output = parse_csv('ImputeTestDataOutput.csv')
        self.assertEqual(len(test_input), len(test_output))
        # Join input and output data
        for k, v in test_input.items():
            v.update(test_output[k])
        first = True
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
        
        for voyage_id, row in test_input.items():
            print 'Testing voyage_id:' + str(voyage_id)
            interim = self.interim_voyage(row)
            all_vars = compute_imputed_vars(interim)[2]
            # Check that the imputed fields all match.
            mismatches = []
            for k, v in all_vars.items():
                if not k in row:
                    if first:
                        print "Missing field: " + k
                    continue
                expected = row[k]
                if is_number(v) or is_number(expected):
                    expected = float(expected) if expected is not None else 0.0
                    if v is None: v = 0.0
                    if abs(v - expected) >= 0.01:
                        mismatches.append((k, expected, v))
                elif v != expected:
                    mismatches.append((k, expected, v))
            if len(mismatches) > 0:
                mismatches = sorted(mismatches, key=lambda m: m[0])
                errors[voyage_id] = 'Mismatches on voyage id ' + voyage_id + ':\n' + \
                    ',\n'.join(['\t' + mismatch_text(m) for m in mismatches]) + \
                    '\nInterim numbers:\n' + str_dict({sn.var_name: sn.number for sn in interim.slave_numbers.all()}) + \
                    '\nInterim:\n' + str_dict(vars(interim)) + \
                    '\nAll variables:\n' + str_dict(all_vars)
            first = False        
        
        if len(errors) > 0:
            print 'Failed ' + str(len(errors)) + '/' + str(len(test_input))
        self.assertEqual(0, len(errors), '\n'.join(errors.values()))
        
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