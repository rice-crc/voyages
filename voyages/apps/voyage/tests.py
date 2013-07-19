from django.test import TestCase
from django.test.utils import override_settings
from .models import VoyageDates

@override_settings(LANGUAGE_CODE='en')
class SimpleGetPageTest(TestCase):
    """
    Test of the get_page in the voyage view for Understanding the Database
    :view:`voyage.get_page`
    """
    def test_valid_pages(self):
        """
        Attempt to load pages in the valid range 1 to 22
        """
        for i in range (1, 9):
            # Test pages c01_s02_p01 to c01_s02_p09
            response = self.client.get("/voyage/c01_s02_p0" + str(i))
            self.assertEqual(response.status_code, 200)
        for i in range (10, 22):
            # Test pages c01_s02_p01 to c01_s02_p09
            response = self.client.get("/voyage/c01_s02_p" + str(i))
            self.assertEqual(response.status_code, 200)
            
    def test_invalid_pages(self):
        """
        Attempt to load invalid pages (whose number does not exist)
        """
        for i in range(-10, 0):
            response = self.client.get("/voyage/c01_s02_p0" + str(i))
            self.assertEqual(response.status_code, 404)
        for i in range(25, 40):
            response = self.client.get("/voyage/c01_s02_p" + str(i))
            self.assertEqual(response.status_code, 404)


class VoyageDatesPeriodsTest(TestCase):
    """
    Test of the calculating period variables in the
    VoyageDates.
    """

    fixtures = ['test_set_200_voyages.json']

    def test_calculate_period_year(self):
        """
        Check returned values of calculated periods.
        """

        voyage_dates_obj = VoyageDates.objects.get(pk=3)
        self.assertEqual(voyage_dates_obj.calculate_year_period(5), 14)
        self.assertEqual(voyage_dates_obj.calculate_year_period(10), 10)
        self.assertEqual(voyage_dates_obj.calculate_year_period(25), 4)
        self.assertEqual(voyage_dates_obj.calculate_year_period(100), 1)

        voyage_dates_obj = VoyageDates.objects.get(pk=180)
        self.assertEqual(voyage_dates_obj.calculate_year_period(5), 67)
        self.assertEqual(voyage_dates_obj.calculate_year_period(10), 36)
        self.assertEqual(voyage_dates_obj.calculate_year_period(25), 15)
        self.assertEqual(voyage_dates_obj.calculate_year_period(100), 4)
