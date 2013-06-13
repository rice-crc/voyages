# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.utils import override_settings
from django.core.management import call_command
from sys import stderr
from .models import Glossary

@override_settings(LANGUAGE_CODE='en')
class GlossaryEmptyTest(TestCase):
    """
    Test for empty glossary
    """

    def test_rendering_response_code(self):
        """
        Test if initial website is rendering properly
        """

        # Check response code
        response = self.client.get('/help/page_glossary')
        self.assertEqual(response.status_code, 200)


@override_settings(LANGUAGE_CODE='en')
class GlossaryInitialTest(TestCase):
    """
    Tests for initial data from glossary
    """
    fixtures = ['glossary.json']
    initial_objects = 0

    def setUp(self):
        self.initial_objects = Glossary.objects.count()

    def test_rendering_response_code(self):
        """
        Test if initial website is rendering properly
        """

        # Check response code
        response = self.client.get('/help/page_glossary')
        self.assertEqual(response.status_code, 200)

    def test_glossary_content(self):
        """
        Test if glossary website contains all initial data
        """

        response = self.client.get('/help/page_glossary')
        for i in Glossary.objects.all():
            self.assertEqual(response, i.term)
            self.assertEqual(response, i.description)


@override_settings(LANGUAGE_CODE='en')
class GlossaryModifiedTest(TestCase):
    """
    Tests for modified data from glossary
    """
    fixtures = ['glossary_tests.json']
    initial_objects = 0

    def setUp(self):
        self.initial_objects = Glossary.objects.count()

    def test_rendering_response_code(self):
        """
        Test if initial website is rendering properly
        """

        # Check response code
        response = self.client.get('/help/page_glossary')
        self.assertEqual(response.status_code, 200)
        print

    def test_glossary_content(self):
        """
        Test if glossary website contains all initial data
        """

        response = self.client.get('/help/page_glossary')
        for i in Glossary.objects.all():
            self.assertContains(response, i.term)
            self.assertContains(response, i.description)

    def test_adding_items(self):
        """
        Test adding glossary items (adding and response)
        """
        # Add two test items
        Glossary.objects.create(term="Albariv", description="His explen prougg tring thience Barce, haffer).")
        Glossary.objects.create(term="Wgsfew", description="Homarro palium was ques: R. Effic fros ru nonamba soccom men unater par?")

        # Check number of objects
        self.assertEqual(Glossary.objects.count(), self.initial_objects + 2)

        # Check added items
        self.assertEqual(Glossary.objects.get(pk=self.initial_objects+1).term, "Albariv")
        self.assertEqual(Glossary.objects.get(pk=self.initial_objects+1).description, "His explen prougg tring thience Barce, haffer).")
        self.assertEqual(Glossary.objects.get(pk=self.initial_objects+2).term, "Wgsfew")
        self.assertEqual(Glossary.objects.get(pk=self.initial_objects+2).description, "Homarro palium was ques: R. Effic fros ru nonamba soccom men unater par?")

        response = self.client.get('/help/page_glossary')
        for i in [Glossary.objects.get(pk=self.initial_objects+1), Glossary.objects.get(pk=self.initial_objects+2)]:
            self.assertContains(response, i.term)
            self.assertContains(response, i.description)

        # Check response code
        response = self.client.get('/help/page_glossary')
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        pass