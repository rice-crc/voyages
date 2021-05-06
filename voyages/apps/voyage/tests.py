from __future__ import absolute_import, unicode_literals

from builtins import range, str
from datetime import date

from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.test.utils import override_settings
from future import standard_library
from mock import patch

from .globals import get_incremented_year_tuples, var_dict

standard_library.install_aliases()


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
        for i in range(1, 22 + 1):
            # Test pages 1 - 22
            response = self.client.get(
                reverse('voyage:understanding-page',
                        kwargs={'name': 'methodology-%s' % str(i)}))
            self.assertEqual(response.status_code, 200)


class ReportingTest(TestCase):
    """
    Tests some functions used for reporting purposes
    """

    def test_incremented_year_tuples(self):
        list25 = [(1501, 1525), (1526, 1550), (1551, 1575), (1576, 1600),
                  (1601, 1625), (1626, 1650), (1651, 1675), (1676, 1700),
                  (1701, 1725), (1726, 1750), (1751, 1775), (1776, 1800),
                  (1801, 1825), (1826, 1850), (1851, 1875)]
        flist25 = [([(str(x[0]) + '-' + str(x[1]), 1)], {
            'var_imp_arrival_at_port_of_dis__range': [x[0], x[1]]
        }) for x in list25]
        self.assertEqual(get_incremented_year_tuples(25, 1514, 1866),
                         flist25)


@override_settings(LANGUAGE_CODE='en')
class SearchTest(TestCase):

    fixtures = [
        'geographical.json', 'shipattributes.json', 'groupings.json',
        'outcomes.json'
    ]
    """
    Tests the search page and associated functions
    """

    def setUp(self):
        self.client = Client()

    def test_search_forms_exist(self):
        response = self.client.get('/voyage/search')
        for var in var_dict:
            var_name = var['var_name']
            thing = 'id="id_' + var_name + '-is_shown_field"'
            if var['is_general'] or var['is_basic']:
                self.assertIn(thing, response.content, msg=var_name)

    @patch('voyages.apps.voyage.views.perform_search')
    def test_search_geographical(self, perform_search_func):
        self.client.get(
            '/voyage/search?'
            'used_variable_names=var_imp_port_voyage_begin&'
            'time_span_from_year=1514&'
            'var_imp_port_voyage_begin_choice_field='
            '60412%3B60803%3B60807%3B60820%3B60833%'
            '3B60834%3B60999%3B50203%3B50299&'
            'time_span_to_year=1866'
        )
        self.assertEqual(len(perform_search_func.call_args_list), 1)
        args = perform_search_func.call_args_list[0][0]
        qdict = args[0]
        self.assertIn('var_imp_port_voyage_begin_idnum__in', qdict)
        expected = [
            60412, 60803, 60807, 60820, 60833, 60834, 60999, 50203, 50299
        ]
        self.assertEqual(
            expected, qdict['var_imp_port_voyage_begin_idnum__in'])

    @patch('voyages.apps.voyage.views.perform_search')
    def test_search_text(self, perform_search_func):
        self.assertEqual(len(perform_search_func.call_args_list), 1)
        args = perform_search_func.call_args_list[0][0]
        qdict = args[0]
        self.assertIn('var_ship_name__contains', qdict)
        self.assertEqual('Ner', qdict['var_ship_name__contains'])

    @patch('voyages.apps.voyage.views.perform_search')
    def test_search_select(self, perform_search_func):
        self.client.get(
            '/voyage/search?'
            'used_variable_names=var_outcome_slaves&'
            'var_outcome_slaves_choice_field=1%3B2%3B3%3B5%3B6&'
            'time_span_from_year=1514&'
            'time_span_to_year=1866'
        )
        self.assertEqual(len(perform_search_func.call_args_list), 1)
        args = perform_search_func.call_args_list[0][0]
        qdict = args[0]
        self.assertIn('var_outcome_slaves_idnum__in', qdict)
        expected = [1, 2, 3, 5, 6]
        self.assertEqual(expected, qdict['var_outcome_slaves_idnum__in'])

    @patch('voyages.apps.voyage.views.perform_search')
    def test_search_numeric(self, perform_search_func):
        self.assertEqual(len(perform_search_func.call_args_list), 1)
        args = perform_search_func.call_args_list[0][0]
        qdict = args[0]
        self.assertIn('var_imp_total_num_slaves_purchased__range', qdict)
        self.assertEqual([u'40', u'2000'],
                         qdict['var_imp_total_num_slaves_purchased__range'])

    @patch('voyages.apps.voyage.views.perform_search')
    def test_search_date(self, perform_search_func):
        self.client.get(
            '/voyage/search?'
            'var_voyage_began_to_month=12&'
            'var_voyage_began_from_month=01&'
            'time_span_from_year=1514&'
            'var_voyage_began_months='
            '01%2C03%2C05%2C06%2C07%2C09%2C10%2C11%2C12&'
            'used_variable_names=var_voyage_began&'
            'time_span_to_year=1866&'
            'var_voyage_began_options=1&'
            'var_voyage_began_from_year=1514&'
            'var_voyage_began_to_year=1866'
        )
        self.assertEqual(len(perform_search_func.call_args_list), 1)
        args = perform_search_func.call_args_list[0][0]
        qdict = args[0]
        self.assertIn('var_voyage_began__range', qdict)
        self.assertIn('var_voyage_began_month__in', qdict)
        self.assertEqual([1, 3, 5, 6, 7, 9, 10, 11, 12],
                         qdict['var_voyage_began_month__in'],
                         "Incorrect months filter")
        self.assertEqual(
            [date(1514, 0o1, 0o1), date(1867, 1, 1)],
            qdict['var_voyage_began__range'], "Incorrect date range")

    @patch('voyages.apps.voyage.views.perform_search')
    def test_search_boolean(self, perform_search_func):
        self.assertEqual(len(perform_search_func.call_args_list), 1)
        args = perform_search_func.call_args_list[0][0]
        qdict = args[0]
        self.assertIn('var_voyage_in_cd_rom__in', qdict)
        self.assertEqual([u'1'], qdict['var_voyage_in_cd_rom__in'])


# don't think the function is being used
# class VoyageDatesPeriodsTest(TestCase):
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
