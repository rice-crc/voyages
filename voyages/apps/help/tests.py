from django.test import TestCase
from .models import Glossary
from django.test.utils import override_settings

@override_settings(LANGUAGE_CODE='en')
class GlossaryTest(TestCase):
    def test_check_empty_glossary(self):

        # Check number of objects
        self.assertEqual(Glossary.objects.count(), 0)

        # Check response code
        response = self.client.get('/help/page_glossary')
        self.assertEqual(response.status_code, 200)

    def initial_view(self):
        response = self.client.get('/help/page_glossary')

        # Test if status code is 200