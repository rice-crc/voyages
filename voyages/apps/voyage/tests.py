"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.test.utils import override_settings

@override_settings(LANGUAGE_CODE='en')
class SimpleTest(TestCase):
    def test_valid_pages(self):
        for i in range (1, 9):
            # Test pages c01_s02_p01 to c01_s02_p09
            response = self.client.get("/voyage/c01_s02_p0" + str(i))
            self.assertEqual(response.status_code, 200)
        for i in range (10, 22):
            # Test pages c01_s02_p01 to c01_s02_p09
            response = self.client.get("/voyage/c01_s02_p" + str(i))
            self.assertEqual(response.status_code, 200)
            
    def test_invalid_pages(self):
        for i in range(-10, 0):
            response = self.client.get("/voyage/c01_s02_p" + str(i))
            self.assertEqual(response.status_code, 404)