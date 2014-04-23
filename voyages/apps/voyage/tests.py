from django.test import TestCase
from django.test.utils import override_settings
from django.test import Client
from .models import VoyageDates
from django.core.urlresolvers import reverse
from .views import shorten_url
from mock import patch
import globals
import urllib2
from datetime import date

@override_settings(LANGUAGE_CODE='en')
class SimpleGetPageTest(TestCase):
    """
    Test of the get_page in the voyage view for Understanding the Methodology
    :view:`voyage.get_page`
    """
    def test_valid_pages(self):
        """
        Attempt to load pages in the valid range 1 to 22
        """
        for i in range (1, 22+1):
            # Test pages 1 - 22
            response = self.client.get(reverse('voyage:understanding-page', kwargs={'name': 'methodology-%s' % str(i)}))
            self.assertEqual(response.status_code, 200)

class UrlShortenerTest(TestCase):
    """
    Test of the shorten_url method that uses bitly to shorten url
    """
    def test_shorten_valid_url(self):
        """
        Attempt to shorten a valid url
        """
        long_url = 'http://www.google.com/'
        short_url = shorten_url(long_url)
        self.assertNotEqual(short_url, long_url)
        try:
            resp = urllib2.urlopen(short_url)
        except:
            self.fail("Invalid url provided by shorten_url method")

    def test_shorten_invalid_url(self):
        """
        Attempt to shorten an invalid url
        """
        long_url = '---adsfasdfafdjgkdf.&^*&5hgvkaadsadsfhgkjfm.com'
        short_url = shorten_url(long_url)
        self.assertEqual(short_url, long_url, "When url is invalid, shorten_url should return the long_url")
class ReportingTest(TestCase):
    """
    Tests some functions used for reporting purposes
    """
    def test_incremented_year_tuples(self):
        list25 = [(1501, 1525), (1526, 1550), (1551, 1575), (1576, 1600),
                  (1601, 1625), (1626, 1650), (1651, 1675), (1676, 1700),
                  (1701, 1725), (1726, 1750), (1751, 1775), (1776, 1800),
                  (1801, 1825), (1826, 1850), (1851, 1875)]
        flist25 = map(lambda x: (str(x[0]) + '-' + str(x[1]), {'var_imp_voyage_began__range': [x[0], x[1]]}), list25)
        self.assertEqual(globals.get_incremented_year_tuples(25, 1514, 1866), flist25)
@override_settings(LANGUAGE_CODE='en')
class SearchTest(TestCase):
    """
    Tests the search page and associated functions
    """
    def setUp(self):
        self.client = Client()
    def test_search_forms_exist(self):
        response = self.client.get('/voyage/search')
        for var in globals.var_dict:
            var_name = var['var_name']
            thing = 'id="id_' + var_name + '-is_shown_field"'
            if var['is_general'] or var['is_basic']:
                self.assertIn(thing, response.content, msg=var_name)
    
    @patch('voyages.apps.voyage.views.perform_search')
    def test_search_geographical(self, perform_search_func):
        self.client.get('/voyage/search?time_span_to_year=1866&used_variable_names=var_imp_port_voyage_begin&var_imp_port_voyage_begin_choice_field=Africa.%2C+port+unspecified%3BBissau%3BGoree%3BPortuguese+Guinea%3BCape+Verde+Islands%3BMadeira%3BAzores%3BSaint-Louis%3BSierra+Leone%2C+port+unspecified%3BBance+Island+%28Ben%27s+Island%29%3BCape+Coast+Castle%3BPrinces+Island%3BSao+Tome%3BSao+Tome+or+Princes+Island%3BLuanda%3BCape+of+Good+Hope%3BInhambane%3BMozambique%3BIle+de+France%3BPort-Louis%3BPuerto+Rico%2C+port+unspecified%3BBahia+Honda%3BCabanas%3BCanasi%3BCardenas%3BGuanimar%3BHavana%3BMatanzas%3BSantiago+de+Cuba%3BTrinidad+de+Cuba%3BCuba%2C+port+unspecified%3BTortola%2C+port+unspecified%3BAntigua%2C+port+unspecified%3BSaint+John+%28Antigua%29%3BSt.+Kitts%2C+port+unspecified%3BNevis%2C+port+unspecified%3BMontserrat%2C+port+unspecified%3BDominica%2C+port+unspecified%3BSt.+Lucia%2C+port+unspecified%3BBarbados%2C+port+unspecified%3BGrenada%2C+port+unspecified%3BTobago%2C+port+unspecified%3BMartha+Brae%3BMontego+Bay%3BKingston%3BJamaica%2C+port+unspecified%3BDemerara%3BMartinique%2C+port+unspecified%3BGuadeloupe%2C+port+unspecified%3BCayenne%3BPort-au-Prince%3BSt.+Maarten%3BSt.+Eustatius%3BHonduras%2C+port+unspecified%3BSt.+Barthelemy%2C+port+unspecified%3BGustavia%2C+St.+Bartholomew%3BDanish+West+Indies%2C+colony+unspecified%3BSt.+Croix%3BSt.+Thomas%3BBritish+Leewards%3BBritish+Caribbean%2C+colony+unspecified%3BBermuda%3BHispaniola%2C+unspecified%3BSpanish+Caribbean%2C+unspecified&time_span_from_year=1514')
        self.assertEqual(len(perform_search_func.call_args_list), 1)
        args = perform_search_func.call_args_list[0][0]
        qdict = args[0]
        self.assertIn('var_imp_port_voyage_begin__in', qdict)
        expected = [u'Africa., port unspecified', u'Bissau', u'Goree', u'Portuguese Guinea', u'Cape Verde Islands', u'Madeira', u'Azores', u'Saint-Louis', u'Sierra Leone, port unspecified', u"Bance Island (Ben's Island)", u'Cape Coast Castle', u'Princes Island', u'Sao Tome', u'Sao Tome or Princes Island', u'Luanda', u'Cape of Good Hope', u'Inhambane', u'Mozambique', u'Ile de France', u'Port-Louis', u'Puerto Rico, port unspecified', u'Bahia Honda', u'Cabanas', u'Canasi', u'Cardenas', u'Guanimar', u'Havana', u'Matanzas', u'Santiago de Cuba', u'Trinidad de Cuba', u'Cuba, port unspecified', u'Tortola, port unspecified', u'Antigua, port unspecified', u'Saint John (Antigua)', u'St. Kitts, port unspecified', u'Nevis, port unspecified', u'Montserrat, port unspecified', u'Dominica, port unspecified', u'St. Lucia, port unspecified', u'Barbados, port unspecified', u'Grenada, port unspecified', u'Tobago, port unspecified', u'Martha Brae', u'Montego Bay', u'Kingston', u'Jamaica, port unspecified', u'Demerara', u'Martinique, port unspecified', u'Guadeloupe, port unspecified', u'Cayenne', u'Port-au-Prince', u'St. Maarten', u'St. Eustatius', u'Honduras, port unspecified', u'St. Barthelemy, port unspecified', u'Gustavia, St. Bartholomew', u'Danish West Indies, colony unspecified', u'St. Croix', u'St. Thomas', u'British Leewards', u'British Caribbean, colony unspecified', u'Bermuda', u'Hispaniola, unspecified', u'Spanish Caribbean, unspecified']
        self.assertEqual(expected, qdict['var_imp_port_voyage_begin__in'])
    @patch('voyages.apps.voyage.views.perform_search')
    def test_search_text(self, perform_search_func):
        response = self.client.get('/voyage/search?time_span_to_year=1866&used_variable_names=var_ship_name&var_ship_name_text_search=Ner&time_span_from_year=1514')
        self.assertEqual(len(perform_search_func.call_args_list), 1)
        args = perform_search_func.call_args_list[0][0]
        qdict = args[0]
        self.assertIn('var_ship_name__contains', qdict)
        self.assertEqual('Ner', qdict['var_ship_name__contains'])
    @patch('voyages.apps.voyage.views.perform_search')
    def test_search_select(self, perform_search_func):
        self.client.get('/voyage/search?time_span_to_year=1866&var_outcome_slaves_choice_field=Slaves+disembarked+in+Americas%3BNo+slaves+embarked%3BSlaves+disembarked+in+Africa%2FEurope%3BSlaves+perished+with+ship&used_variable_names=var_outcome_slaves&time_span_from_year=1514')
        self.assertEqual(len(perform_search_func.call_args_list), 1)
        args = perform_search_func.call_args_list[0][0]
        qdict = args[0]
        self.assertIn('var_outcome_slaves__in', qdict)
        expected = [u'Slaves disembarked in Americas', u'No slaves embarked', u'Slaves disembarked in Africa/Europe', u'Slaves perished with ship']
        self.assertEqual(expected, qdict['var_outcome_slaves__in'])
    @patch('voyages.apps.voyage.views.perform_search')
    def test_search_numeric(self, perform_search_func):
        response = self.client.get('/voyage/search?var_imp_total_num_slaves_purchased_lower_bound=40&time_span_from_year=1514&var_imp_total_num_slaves_purchased_upper_bound=2000&var_imp_total_num_slaves_purchased_options=1&used_variable_names=var_imp_total_num_slaves_purchased&time_span_to_year=1866')
        self.assertEqual(len(perform_search_func.call_args_list), 1)
        args = perform_search_func.call_args_list[0][0]
        qdict = args[0]
        self.assertIn('var_imp_total_num_slaves_purchased__range', qdict)
        self.assertEqual([u'40', u'2000'], qdict['var_imp_total_num_slaves_purchased__range'])
    @patch('voyages.apps.voyage.views.perform_search')
    def test_search_date(self, perform_search_func):
        self.client.get('/voyage/search?var_voyage_began_to_month=12&var_voyage_began_from_month=01&time_span_from_year=1514&var_voyage_began_months=01%2C03%2C05%2C06%2C07%2C09%2C10%2C11%2C12&used_variable_names=var_voyage_began&time_span_to_year=1866&var_voyage_began_options=1&var_voyage_began_from_year=1514&var_voyage_began_to_year=1866')
        self.assertEqual(len(perform_search_func.call_args_list), 1)
        args = perform_search_func.call_args_list[0][0]
        qdict = args[0]
        self.assertIn('var_voyage_began__range', qdict)
        self.assertIn('var_voyage_began_month__in', qdict)
        self.assertEqual([1,3,5,6,7,9,10,11,12], qdict['var_voyage_began_month__in'], "Incorrect months filter")
        self.assertEqual([date(1514,01,01), date(1866,12,31)], qdict['var_voyage_began__range'], "Incorrect date range")
    @patch('voyages.apps.voyage.views.perform_search')
    def test_search_boolean(self, perform_search_func):
        response = self.client.get('/voyage/search?time_span_to_year=1866&used_variable_names=var_voyage_in_cd_rom&var_voyage_in_cd_rom_choice_field=1&time_span_from_year=1514')
        self.assertEqual(len(perform_search_func.call_args_list), 1)
        args = perform_search_func.call_args_list[0][0]
        qdict = args[0]
        self.assertIn('var_voyage_in_cd_rom__in', qdict)
        self.assertEqual([u'1'], qdict['var_voyage_in_cd_rom__in'])
    
    
#don't think the function is being used 
#class VoyageDatesPeriodsTest(TestCase):
#    """
#    Test of the calculating period variables in the
#    VoyageDates.
#    """
#
#    fixtures = ['test_set_200_voyages.json']
#
#    def test_calculate_period_year(self):
#        """
#        Check returned values of calculated periods.
#        """
#
#        voyage_dates_obj = VoyageDates.objects.get(pk=3)
#        self.assertEqual(voyage_dates_obj.calculate_year_period(5), 14)
#        self.assertEqual(voyage_dates_obj.calculate_year_period(10), 10)
#        self.assertEqual(voyage_dates_obj.calculate_year_period(25), 4)
#        self.assertEqual(voyage_dates_obj.calculate_year_period(100), 1500)
#
#        voyage_dates_obj = VoyageDates.objects.get(pk=180)
#        self.assertEqual(voyage_dates_obj.calculate_year_period(5), 67)
#        self.assertEqual(voyage_dates_obj.calculate_year_period(10), 36)
#        self.assertEqual(voyage_dates_obj.calculate_year_period(25), 15)
#        self.assertEqual(voyage_dates_obj.calculate_year_period(100), 1800)
