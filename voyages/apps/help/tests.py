# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
import random
import haystack
from voyages.apps.help.models import Glossary, Faq, FaqCategory
import mock


class TestGlossarySearch(TestCase):
    """
    Post a query with a key word that would NOT generate a result
    because Solr is not updated
    """
    fixtures = ['glossary.json']

    @override_settings(LANGUAGE_CODE='en')
    def test_search_noresult(self):
        """
        Should not display any matching record
        """
        for i in range(1, 10):
            no_res_query = 'abcdefgh-willnotappear' + str(random.randint(0,10000000))
            response = self.client.post(reverse('help:glossary'), {'q' : no_res_query})
            self.assertEqual(response.status_code, 200)
            # The result should appear only once (in the search field)
            self.assertContains(response, no_res_query, 1)


class TestFaqSearch(TestCase):
    """
    Simple test of the search engine
    """
    fixtures = ['faq_data_all.json']
    
    @override_settings(HAYSTACK_CONNECTIONS = {'default': {'ENGINE': 'haystack.backends.simple_backend.SimpleEngine','SILENTLY_FAIL': True,},})
    @override_settings(LANGUAGE_CODE='en')
    def test_search_noresult(self):
        """
        Should not display any matching record
        """
        for i in range(1, 10):
            no_res_query = 'abcdefgh-willnotappear' + str(random.randint(0,10000000))
            response = self.client.post(reverse('help:faqs'), {'q' : no_res_query})
            self.assertEqual(response.status_code, 200)
            # The result should appear only once (in the search field)
            self.assertContains(response, no_res_query, 1)

    @override_settings(HAYSTACK_CONNECTIONS = {'default': {'ENGINE': 'haystack.backends.simple_backend.SimpleEngine','SILENTLY_FAIL': True,},})
    @override_settings(LANGUAGE_CODE='en')
    def test_not_using_realtime(self):
        """
        Post a query with a key word that would NOT generate a result
        because Solr is not updated
        """
        prefix_question = "panda question "
        prefix_answer = "giraffe answer "
        loop_count = 10    
            
        for i in range(1, loop_count):
            faq_item_question = prefix_question + str(random.randint(0, 10000))
            faq_item_answer = prefix_answer + str(random.randint(0, 1000000))
            faq_item_question_order = random.randint(10,20)
            faq_item_category = FaqCategory.objects.order_by('?')[0]
    
            # Generate a FAQ
            faq_item = Faq.objects.create(question=faq_item_question, answer=faq_item_answer, 
                        question_order=faq_item_question_order, category=faq_item_category)
                
        response = self.client.post(reverse('help:faqs'), { 'q': 'panda',})
        # The only matching text is the text in the search box itself
        self.assertContains(response, 'panda' , loop_count)
