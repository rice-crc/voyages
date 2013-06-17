# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
import random
import haystack
from .models import Glossary, Faq, FaqCategory

#
# Test for the FAQ model
#
@override_settings(LANGUAGE_CODE='en')
class TestEmptyFaq(TestCase):
    """
    Test when FAQ contains no record
    """
    def test_rendering_response_code(self):
        """
        Test if initial website is rendering properly
        """

        # Check response code
        response = self.client.get(reverse('help:faqs'))
        self.assertEqual(response.status_code, 200)

@override_settings(LANGUAGE_CODE='en')
@override_settings(HAYSTACK_CONNECTIONS = {'default': {'ENGINE': 'haystack.backends.simple_backend.SimpleEngine','SILENTLY_FAIL': True,},})
class TestFaqAllData(TestCase):
    """
    Tests on the full dataset of FAQ
    """
    fixtures = ['faq_data_all.json']

    def test_rendering_response_code(self):
        """
        Test if initial website is rendering properly
        """
        # Check response code
        response = self.client.get(reverse('help:faqs'))
        self.assertEqual(response.status_code, 200)

    def test_contain_words(self):
        """
        Test if the page displays all FAQs
        """
        response = self.client.get(reverse('help:faqs'))
        for item in Faq.objects.all():
            self.assertContains(response, item.question)
            self.assertContains(response, item.answer)
        for category in FaqCategory.objects.all():
            self.assertContains(response, category.text)

@override_settings(HAYSTACK_CONNECTIONS = {'default': {'ENGINE': 'haystack.backends.simple_backend.SimpleEngine','SILENTLY_FAIL': True,},})
@override_settings(LANGUAGE_CODE='en')
class TestFaqModification(TestCase):
    """
    Modification test on FAQs
    """
    fixtures = ['faq_data_all.json']

    def test_adding_new_faqs(self):
        """
        Test adding several random new FAQs
        """
        objectList = []
        for i in range(0, 20):
            faq_item_question = "test_text_question_" + str(random.randint(0, 1000000))
            faq_item_answer = "test_text_answer_" + str(random.randint(0, 1000000))
            faq_item_question_order = random.randint(100,200)
            faq_item_category = FaqCategory.objects.order_by('?')[0]
            
            # Generate a FAQ
            faq_item = Faq.objects.create(question=faq_item_question, answer=faq_item_answer, 
                    question_order=faq_item_question_order, category=faq_item_category)
            objectList.append(faq_item)
        
        # Check whether the FAQ page contains the new FAQs recently added
        response = self.client.get(reverse('help:faqs'))
        self.assertEqual(response.status_code, 200)
        for faq_test_item in objectList:
            self.assertContains(response, faq_test_item.question)
            self.assertContains(response, faq_test_item.answer)
        for i in objectList:
            i.delete()
            
    def test_deleting_faqs(self):
        """
        Test deleting FAQs
        """
        questionList = []
        answerList = []
        # Delete random FAQs
        for i in range(0, 10):
            faq_item = Faq.objects.order_by('?')[0]
            questionList.append(faq_item.question)
            answerList.append(faq_item.answer)
            faq_item.delete()
        
        response = self.client.get(reverse('help:faqs'))
        self.assertEqual(response.status_code, 200)
        for text in questionList:
            self.assertNotContains(response, text)
        for text in answerList:
            self.assertNotContains(response, text)
            
    def test_deleting_entire_category(self):
        """
        Test deleting all FAQs belonging to a category
        """
        faq_category = FaqCategory.objects.order_by('?')[0]
        list_questions = Faq.objects.filter(category=faq_category)
        
        questionList = []
        answerList = []
        # Delete random FAQs
        for faq_item in list_questions:
            questionList.append(faq_item.question)
            answerList.append(faq_item.answer)
            faq_item.delete()
        
        response = self.client.get(reverse('help:faqs'))
        self.assertNotContains(response, faq_category.text)

@override_settings(LANGUAGE_CODE='en')
class TestFaqSearch(TestCase):
    """
    Simple test of the search engine
    """
    fixtures = ['faq_data_all.json']
    
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


@override_settings(HAYSTACK_SIGNAL_PROCESSOR='haystack.signals.RealtimeSignalProcessor')
@override_settings(LANGUAGE_CODE='en')
class TestFaqSearchRealTime(TestCase):
    """
    Simple test of the search engine using real time processing to reach Solr
    """
    fixtures = ['faq_data_all.json']
    
    def setUp(self):
        self._haystack_backend = haystack.backend
        haystack.backend = haystack.load_backend('simple')

    def tearDown(self):
        haystack.backend = self._haystack_backend
    
    def not_in_use_test_search_with_results(self):
        """
        Post a query with a key word that would generate a result
        """
        
        prefix_question = "panda question "
        prefix_answer = "giraffe answer "
        loop_count = 10    
        
        # Use the real time processor
        objectList = []
        settings.HAYSTACK_SIGNAL_PROCESSOR='haystack.signals.RealtimeSignalProcessor'
        print "Settings: %s" % settings.HAYSTACK_SIGNAL_PROCESSOR
        
        for i in range(1, loop_count):
            faq_item_question = prefix_question + str(random.randint(0, 10000))
            faq_item_answer = prefix_answer + str(random.randint(0, 1000000))
            faq_item_question_order = random.randint(10,20)
            faq_item_category = FaqCategory.objects.order_by('?')[0]
           
            # Generate a FAQ
            faq_item = Faq.objects.create(question=faq_item_question, answer=faq_item_answer, 
                            question_order=faq_item_question_order, category=faq_item_category)
            objectList.append(faq_item)
        
        response = self.client.post(reverse('help:faqs'), { 'q': 'panda',})
        self.assertContains(response, 'panda' , loop_count + 1)
        for obj in objectList:
            # Remove the object (from Solr as well)
            obj.delete()
