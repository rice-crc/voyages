from django.test import TestCase
from django.test.utils import override_settings
from .models import VoyageDates
from django.core.urlresolvers import reverse

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
