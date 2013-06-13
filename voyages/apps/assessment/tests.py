from django.test import TestCase
from django.test.utils import override_settings

@override_settings(LANGUAGE_CODE='en')
class SimpleGetPageTest(TestCase):
    """
    Test of the get_page in the assessment view for Essays
    :view:`assessment.get_page`
    """
    prefixsect1 = "/assessment/c01_s01_p"
    prefixsect2 = "/assessment/c01_s02_p"
    def check_valid(url):
        response = self.client.get(url)
        response.assertEqual(response.status_code, 200)
        
    def check_invalid(url):
        response = self.client.get(url)
        response.assertEqual(response.status_code, 404)
    
    def test_valid_pages(self):
        """
        Attempt to load pages in the valid range 1 to 11 for section 1, 1 to 9 for section 2
        """
        for i in range (1, 9):
            # Test pages c01_s01_p01 to c01_s01_p09
            check_valid(prefixsect1 + "0" + str(i))
        for i in range (10, 11):
            # Test pages c01_s01_p10 to c01_s01_p11
            check_valid(prefixsect1 + str(i))
        for i in range (1, 9):
            # Test pages c01_s01_p01 to c01_s01_p09
            check_valid(prefixsect2 + "0" + str(i))
            
    def test_invalid_pages(self):
        """
        Attempt to load invalid pages (whose number does not exist)
        """
        for i in range(-10, 0):
            check_invalid(self, prefixsect1 + "0" + str(i))
            check_invalid(self, prefixsect1 + str(i))
        for i in range(12, 30):
            check_invalid(self, prefixsect1 + "0" + str(i))
            check_invalid(self, prefixsect1 + str(i))
        for i in range(-10, 0):
            check_invalid(self, prefixsect2 + "0" + str(i))
            check_invalid(self, prefixsect2 + str(i))
        for i in range(10, 30):
            check_invalid(self, prefixsect2 + "0" + str(i))
            check_invalid(self, prefixsect2 + str(i))