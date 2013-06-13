from django.test import TestCase
from django.test.utils import override_settings

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
            response = self.client.get("/voyage/c01_s02_p" + str(i))
            self.assertEqual(response.status_code, 404)
        for i in range(23, 40):
            response = self.client.get("/voyage/c01_s02_p" + str(i))
            self.assertEqual(response.status_code, 404)