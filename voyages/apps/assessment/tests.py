from __future__ import unicode_literals

from builtins import range, str

from django.test import TestCase
from django.test.utils import override_settings


@override_settings(LANGUAGE_CODE='en')
class SimpleGetPageTest(TestCase):
    """
    Test of the get_page in the assessment view for Essays
    :view:`assessment.get_page`
    """
    prefix_sect_1 = "/assessment/c01_s01_p"
    prefix_sect_2 = "/assessment/c01_s02_p"

    def check_valid(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def check_invalid(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_valid_pages(self):
        """
        Attempt to load pages in the valid range 1 to 11 for section 1, 1 to 9
        for section 2
        """
        for i in range(1, 9):
            # Test pages c01_s01_p01 to c01_s01_p09
            self.check_valid(self.prefix_sect_1 + "0" + str(i))
        for i in range(10, 11):
            # Test pages c01_s01_p10 to c01_s01_p11
            self.check_valid(self.prefix_sect_1 + str(i))
        for i in range(1, 9):
            # Test pages c01_s01_p01 to c01_s01_p09
            self.check_valid(self.prefix_sect_2 + "0" + str(i))

    def test_invalid_pages(self):
        """
        Attempt to load invalid pages (whose number does not exist)
        """
        for i in range(-10, 0):
            self.check_invalid(self.prefix_sect_1 + "0" + str(i))
            self.check_invalid(self.prefix_sect_1 + str(i))
        for i in range(1000, 1009):
            self.check_invalid(self.prefix_sect_1 + "0" + str(i))
            self.check_invalid(self.prefix_sect_1 + str(i))
        for i in range(-10, 0):
            self.check_invalid(self.prefix_sect_2 + "0" + str(i))
            self.check_invalid(self.prefix_sect_2 + str(i))
        for i in range(1000, 1009):
            self.check_invalid(self.prefix_sect_2 + "0" + str(i))
            self.check_invalid(self.prefix_sect_2 + str(i))
