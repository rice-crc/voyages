from django.test import TestCase, TransactionTestCase
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

class TestEditorialPlatform(TransactionTestCase):
    """
    Here we will test the editorial platform by creating mock
    user contributions and following possible editorial workflows
    until their conclusion (e.g. publication).
    """
    
    fixtures = ['geographical.json', 'shipattributes.json', 'groupings.json', 'outcomes.json', 'testvoyages.json']
    
    def test_workflow(self):
    
        # Create a user for the contributor.
        the_password = 'mypass'
        contributor = User.objects.create_user(username='contributor', password=the_password)
        
        # Create a reviewer user
        reviewer = User.objects.create_user(username='reviewer', password=the_password)
        
        # Create an editor user
        editor = User.objects.create_superuser('editor', 'editor@voyages.org', the_password)
        
        def login(user):
            self.client.logout()
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
        interim.ship_construction_place = Place.objects.get(pk=51)
        interim.ship_registration_place = Place.objects.get(pk=51)
        interim.national_carrier = Nationality.objects.get(pk=7)
        interim.rig_of_vessel = RigOfVessel.objects.get(pk=1)
        interim.tonnage_of_vessel = 200
        interim.ton_type = TonType.objects.get(pk=21)
        interim.guns_mounted = 21
        interim.first_ship_owner = "Smart, Jonathan"
        interim.second_ship_owner = "Spring, Martin"
        interim.additional_ship_owners = "McCall, Seamus"
        interim.voyage_outcome = ParticularOutcome.objects.get(pk=1)
        interim.african_resistance = Resistance.objects.get(pk=5)
        interim.first_port_intended_embarkation = Place.objects.get(pk=522)
        interim.second_port_intended_embarkation = Place.objects.get(pk=539)
        interim.first_port_intended_disembarkation = Place.objects.get(pk=372)
        interim.port_of_departure = Place.objects.get(pk=51)
        interim.number_of_ports_called_prior_to_slave_purchase = 1
        interim.first_place_of_slave_purchase = Place.objects.get(pk=519)
        interim.second_place_of_slave_purchase = Place.objects.get(pk=523)
        interim.principal_place_of_slave_purchase = Place.objects.get(pk=523)
        interim.place_of_call_before_atlantic_crossing = Place.objects.get(pk=667)
        interim.number_of_new_world_ports_called_prior_to_disembarkation = 1
        interim.first_place_of_landing = Place.objects.get(pk=728)
        interim.second_place_of_landing = Place.objects.get(pk=342)
        interim.principal_place_of_slave_disembarkation = Place.objects.get(pk=728)
        interim.date_departure = "1,30,1646"
        interim.date_slave_purchase_began = "4,22,1646"
        interim.date_vessel_left_last_slaving_port = "6,23,1646"
        interim.date_first_slave_disembarkation = "9,30,1646"
        interim.date_second_slave_disembarkation = "11,4,1646"
        interim.date_third_slave_disembarkation = ",,"
        interim.date_return_departure = "2,15,1647"
        interim.date_voyage_completed = "6,1,1647"
        interim.length_of_middle_passage = 100
        interim.first_captain = "Ribbles, Sam"
        interim.second_captain = "Wood, John"
        interim.third_captain = "Inglis, Henry"
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
            u'interim_slave_number_MEN6': 20.0,
            u'interim_slave_number_MEN4': 12.0,
            u'interim_slave_number_CREW5': 11.0,
            u'interim_slave_number_CREW2': 19.0,
            u'interim_slave_number_CREW3': 17.0,
            u'interim_slave_number_CREW1': 25.0,
            u'interim_slave_number_GIRL4': 10.0,
            u'interim_slave_number_GIRL6': 8.0,
            u'interim_slave_number_GIRL1': 18.0,
            u'interim_slave_number_CREW4': 12.0,
            u'interim_slave_number_GIRL3': 5.0,
            u'interim_slave_number_GIRL2': 5.0,
            u'interim_slave_number_WOMEN6': 10.0,
            u'interim_slave_number_SLINTEN2': 50.0,
            u'interim_slave_number_SLAARRIV': 198.0,
            u'interim_slave_number_MEN2': 12.0,
            u'interim_slave_number_WOMEN4': 12.0,
            u'interim_slave_number_WOMEN2': 12.0,
            u'interim_slave_number_WOMEN3': 42.0,
            u'interim_slave_number_SLAS36': 48.0,
            u'interim_slave_number_WOMEN1': 60.0,
            u'interim_slave_number_TSLAVESP': 248.0,
            u'interim_slave_number_MEN1': 75.0,
            u'interim_slave_number_NCAR13': 190.0,
            u'interim_slave_number_TSLAVESD': 234.0,
            u'interim_slave_number_SLADAFRI': 14.0,
            u'interim_slave_number_BOY1': 37.0,
            u'interim_slave_number_NDESERT': 1.0,
            u'interim_slave_number_SAILD5': 1.0,
            u'interim_slave_number_SAILD4': 2.0,
            u'interim_slave_number_SAILD3': 2.0,
            u'interim_slave_number_SAILD2': 5.0,
            u'interim_slave_number_SAILD1': 2.0,
            u'interim_slave_number_CREWDIED': 10.0,
            u'interim_slave_number_MEN3': 65.0,
            u'interim_slave_number_SLINTEND': 200.0,
            u'interim_slave_number_BOY2': 5.0,
            u'interim_slave_number_BOY3': 25.0,
            u'interim_slave_number_BOY4': 10.0,
            u'interim_slave_number_BOY6': 10.0,
            u'interim_slave_number_NCAR15': 44.0,
            u'interim_slave_number_SLAS32': 150.0
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
        
        ajax_data['submit_val'] = ''
        contrib_args = {'contribution_type': 'new', 'contribution_id': contribution.pk}
        response = self.client.post(reverse('contribute:interim', kwargs=contrib_args), ajax_data)
        self.assertEqual(response.status_code, 200) # not a redirect since there are no sources for this contribution.
        
        # Now submit sources.
        source_type_inverse = {v: k for k, v in source_type_dict.items()}
        new_sources = [
            {u'place_of_publication': u'Cambridge', u'information': None, u'source_ref_text': None,
             u'page_end': 34, u'book_title': u'Transatlantic History', u'url': None, u'publisher': u'CUP',
             u'year': 2015, u'created_voyage_sources': None, u'source_is_essay_in_book': True,
             u'editors': u'Jenkins, Frederick', u'authors': u'Fellows, John', u'essay_title': u'Early English Slave Trade', 
             u'page_start': 33, u'pk': None, u'created_voyage_sources_id': None, u'source_ref_text': None,
             u'type': source_type_inverse[InterimBookSource], u'__index': 1}
        ]
        sources = new_sources
        ajax_data['sources'] = json.dumps(sources)
        response = self.client.post(reverse('contribute:interim', kwargs=contrib_args), ajax_data, follow=True)
        self.assertRedirects(response, reverse('contribute:interim_summary', kwargs=contrib_args), status_code=302, target_status_code=200)
        self.assertTrue(response.content.find('Transatlantic History') > 0)
        self.assertTrue(response.content.find('London') > 0)
        self.assertTrue(response.content.find('Great Britain') > 0)
        
        # Commit submission.
        response = self.client.post(reverse('contribute:interim_commit', kwargs=contrib_args), follow=True)
        self.assertRedirects(response, reverse('contribute:thanks'), status_code=302, target_status_code=200)
        
        # Check backend data.
        contribution = NewVoyageContribution.objects.get(pk=contribution.pk)
        self.assertEqual(contribution.contributor.username, 'contributor')
        self.assertEqual(contribution.status, ContributionStatus.committed)
        interim = contribution.interim_voyage
        self.assertEqual(interim.first_ship_owner, "Smart, Jonathan")
        self.assertEqual(interim.guns_mounted, 21)
        self.assertEqual(interim.voyage_outcome.pk, 1)
        sources = list(interim.book_sources.all())
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0].place_of_publication, u'Cambridge')
        self.assertEqual(sources[0].authors, u'Fellows, John')
        
        # Switch to editor and begin editorial review for contribution.
        login(editor)
        json_response = self.client.get(reverse('contribute:json_pending_requests'))
        parsed_response = json.loads(json_response.content)
        self.assertEqual(len(parsed_response), 1)
        self.assertTrue('new/' + str(contribution.pk) in parsed_response)
        data = parsed_response.values()[0]
        self.assertEqual([u'Lion'], data['voyage_ship'])
        
        json_response = self.client.post(reverse('contribute:begin_editorial_review'), {'contribution_id': 'new/' + str(contribution.pk)})
        parsed_response = json.loads(json_response.content)
        review_request_id = parsed_response.get('review_request_id', 0)
        editor_contribution_id = parsed_response.get('editor_contribution_id', 0)
        self.assertTrue(review_request_id > 0)
        self.assertTrue(parsed_response.get('editor_contribution_id', 0) > 0)
        
        # Access the editorial page.
        response = self.client.get(reverse('contribute:editorial_review', kwargs={'review_request_id': review_request_id}))
        data = response.context
        self.assertEqual(contribution.pk, data['contribution'].pk)
        self.assertItemsEqual(slave_numbers, data['numbers'])
        editor_interim = data['interim']
        self.assertNotEqual(interim.pk, editor_interim.pk)
        self.assertEqual(editor_interim.name_of_vessel, u'Lion')
        self.assertEqual(editor_interim.second_ship_owner, "Spring, Martin")
        self.assertEqual(editor_interim.date_departure, "1,30,1646")
        editor_sources = get_all_new_sources_for_interim(editor_interim.pk)
        self.assertEqual(1, len(editor_sources))
        source = editor_sources[0]
        self.assertEqual(source.place_of_publication, u'Cambridge')
        self.assertEqual(source.authors, u'Fellows, John')
        editor_numbers = {prefix + x.var_name: x.number for x in editor_interim.slave_numbers.all()}
        self.assertDictEqual(slave_numbers, editor_numbers)
        # Impute data.
        ajax_data['editorial_decision'] = u'Should accept this contribution in the test'
        json_response = self.client.post(reverse('contribute:impute_contribution', kwargs={'editor_contribution_id': editor_contribution_id}), ajax_data)
        parsed_response = json.loads(json_response.content)
        self.assertEqual('OK', parsed_response['result'])
        
        expected_imputed_numbers = {u'MEN4': 12.0, u'SLAVEMX7': 185.0, u'MEN6': 20.0, u'MEN7': 85.0, u'MEN1': 75.0, u'MEN2': 12.0, u'MEN3': 65.0, u'ADLT3IMP': 137.0, u'WOMEN1': 60.0, u'WOMEN2': 12.0, u'WOMEN3': 42.0, u'WOMEN4': 12.0, u'WOMEN6': 10.0, u'WOMEN7': 52.0, u'MALE2IMP': 17.0, u'SLAS36': 48.0, u'SLAS32': 150.0, u'FEML1IMP': 100.0, u'SLAVEMX3': 185.0, u'SLAARRIV': 198.0, u'SLAVEMA1': 234.0, u'SLAVEMA3': 185.0, u'ADLT2IMP': 24.0, u'SLAVEMA7': 185.0, u'CHILD7': 48.0, u'SLADAFRI': 14.0, u'CHIL3IMP': 48.0, u'SLAVMAX3': 185.0, u'SLAVMAX1': 234.0, u'BOYRAT3': 0.189189189189189, u'CHIL2IMP': 10.0, u'BOYRAT1': 0.200854700854701, u'SAILD5': 1.0, u'SAILD4': 2.0, u'SAILD1': 2.0, u'SAILD3': 2.0, u'SAILD2': 5.0, u'BOY2': 5.0, u'BOY3': 25.0, u'BOY1': 37.0, u'BOY6': 10.0, u'BOY7': 35.0, u'BOY4': 10.0, u'CREWDIED': 10.0, u'VYMRTIMP': 36.0, u'MENRAT3': 0.459459459459459, u'VYMRTRAT': 0.153846153846154, u'TSLMTIMP': 234.0, u'NDESERT': 1.0, u'FEMALE7': 65.0, u'MALE1IMP': 134.0, u'MALRAT3': 0.648648648648649, u'MALRAT1': 0.572649572649573, u'MALRAT7': 0.648648648648649, u'ADLT1IMP': 159.0, u'TSLAVESD': 234.0, u'TSLAVESP': 248.0, u'CHILRAT1': 0.320512820512821, u'CHILRAT3': 0.259459459459459, u'CHILRAT7': 0.259459459459459, u'WOMRAT3': 0.281081081081081, u'WOMRAT1': 0.307692307692308, u'WOMRAT7': 0.281081081081081, u'BOYRAT7': 0.189189189189189, u'GIRLRAT7': 0.0702702702702703, u'GIRLRAT1': 0.11965811965812, u'GIRLRAT3': 0.0702702702702703, u'SLINTEN2': 50.0, u'SLAVMAX7': 185.0, u'CREW4': 12.0, u'CREW5': 11.0, u'FEML2IMP': 17.0, u'CREW1': 25.0, u'CREW2': 19.0, u'CREW3': 17.0, u'SLAVEMX1': 234.0, u'MENRAT7': 0.459459459459459, u'MENRAT1': 0.371794871794872, u'MALE7': 120.0, u'CHIL1IMP': 75.0, u'SLINTEND': 200.0, u'ADULT7': 137.0, u'GIRL7': 13.0, u'GIRL6': 8.0, u'GIRL4': 10.0, u'GIRL3': 5.0, u'GIRL2': 5.0, u'GIRL1': 18.0, u'MALE3IMP': 120.0, u'NCAR13': 190.0, u'FEML3IMP': 65.0, u'NCAR15': 44.0}

        editor_interim = InterimVoyage.objects.get(pk=editor_interim.pk)
        editor_numbers = {x.var_name: x.number for x in editor_interim.slave_numbers.all()}
        
        def are_same_numbers(d1, d2, delta):
            keys = list(set(d1.keys()) | set(d2.keys()))
            failures = []
            for k in keys:
                v1 = d1.get(k)
                v2 = d2.get(k)
                if v1 == v2: continue
                if (v1 is None) != (v2 is None) or abs(v1 - v2) > delta: 
                    failures.append(str(k) + ': ' + str(v1) + ' vs ' + str(v2))
            self.assertEqual(len(failures), 0, ', '.join(failures) + '\n\n\n' + str(parsed_response['imputed_numbers']))
        
        for k in slave_number_var_names:
            self.assertAlmostEqual(expected_imputed_numbers.get(k.upper(), -1), parsed_response['imputed_numbers'][k], msg=str(k), delta=0.001)
        are_same_numbers(expected_imputed_numbers, editor_numbers, 0.001)
        
        # If we try to accept the contribution, it should fail since the new reference is not yet created.
        submit_data = {
            'editorial_decision': ReviewRequestDecision.accepted_by_editor,
            'created_voyage_id': 99999,
            'decision_message': u'Approving new voyage in testing'}
        json_response = self.client.post(
            reverse('contribute:submit_editorial_decision', kwargs={'editor_contribution_id': editor_contribution_id}),
            submit_data)
        parsed_response = json.loads(json_response.content)
        self.assertEqual(parsed_response['result'], 'Failed')
        
        # Now we create the source reference.
        source_post_data = {'interim_source[' + str(k) + ']': v for k, v in new_sources[0].items() if v is not None}
        source_post_data['mode'] = 'new'
        response = self.client.post(reverse('contribute:editorial_sources'), source_post_data)
        data = response.context
        form = data['form']
        # The form should correspond to a VoyageSourcesAdminForm initialized with our fictitious info.
        form_p = form.as_p()
        self.assertTrue(form_p.find('Transatlantic History') > 0)
        self.assertTrue(form_p.find('Fellows, John') > 0)
        self.assertTrue(form_p.find('(Cambridge, 2015)') > 0)
        
        source_post_data = form.initial.copy()
        source_post_data['mode'] = 'save'
        source_post_data['short_ref'] = 'TEST_SOURCE_1'
        source_post_data['connection_ref'] = 'TEST_SOURCE_1;DUMMY CONN REF'
        editor_sources = get_all_new_sources_for_interim(editor_interim.pk)
        self.assertEqual(1, len(editor_sources))
        source = editor_sources[0]
        source_post_data['interim_source_id'] = new_sources[0]['type'] + '/' + str(source.pk)
        json_response = self.client.post(reverse('contribute:editorial_sources'), source_post_data)
        parsed_response = json.loads(json_response.content)
        self.assertEqual(parsed_response['result'], 'OK', str(parsed_response.get('errors')))
        created_voyage_sources_id = parsed_response['created_voyage_sources_id']
        created_source = VoyageSources.objects.get(pk=created_voyage_sources_id)
        self.assertEqual(created_source.short_ref, 'TEST_SOURCE_1')
        self.assertTrue(created_source.full_ref.find('Transatlantic History') > 0)
        self.assertEqual(created_source.source_type.group_name, 'Published source')