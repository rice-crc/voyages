
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from .models import *
import random

@override_settings(LANGUAGE_CODE='en')
class TestAllData(TestCase):
    """
    Simple test of the Education: Lesson plan view
    """
    fixtures = ['help_lessonplan_data_all.json',]
    def test_simple_rendering_lessonplan_view(self):
        """
        Test simple rendering of the page
        """
        response = self.client.get(reverse('education:lesson-plans'))
        self.assertEqual(response.status_code, 200)
        
    def test_not_empty_lessonplan(self):
        """
        Test that the loaded fixture is non-empty (for other test to work)
        """
        listAllObjects = LessonPlan.objects.all()
        self.assertEqual(len(listAllObjects) > 0, True)
        
    def test_word_contains(self):
        """
        Test whether words really appears on the page
        """
        response = self.client.get(reverse('education:lesson-plans'))
        for lessonplan_item in LessonPlan.objects.all():
            self.assertContains(response, lessonplan_item.text)
            self.assertContains(response, lessonplan_item.author)
            self.assertContains(response, lessonplan_item.grade_level)
            self.assertContains(response, lessonplan_item.course)
            self.assertContains(response, lessonplan_item.key_words)
        for std_type_item in LessonStandardType.objects.all():
            self.assertContains(response, std_type_item.type)
        for lessonstandard_item in LessonStandard.objects.all():
            self.assertContains(response, lessonstandard_item.text)

@override_settings(LANGUAGE_CODE='en')    
class TestNoData(TestCase):
    """
    Simple test on an empty set of lesson plans
    (no fixture loaded)
    """
    def test_empty_lessonplan(self):
        response = self.client.get(reverse('education:lesson-plans'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Abstract")
        self.assertNotContains(response, "Author")
        self.assertNotContains(response, "Course")

@override_settings(LANGUAGE_CODE='en')    
class TestSmallerSubset(TestCase):
    """
    Simple test on a subset of the lesson plan data
    """
    fixtures = ['help_lessonplan_data_part1.json']
    def test_simple_rendering_subset(self):
        """
        Test simple rendering of the page
        """
        response = self.client.get(reverse('education:lesson-plans'))
        self.assertEqual(response.status_code, 200)
    
    def test_word_contains(self):
        """
        Test whether words really appears on the page
        """
        response = self.client.get(reverse('education:lesson-plans'))
        for lessonplan_item in LessonPlan.objects.all():
            self.assertContains(response, lessonplan_item.text)
            self.assertContains(response, lessonplan_item.author)
            self.assertContains(response, lessonplan_item.grade_level)
            self.assertContains(response, lessonplan_item.course)
            self.assertContains(response, lessonplan_item.key_words)
    
    def test_adding_new_lesson_plan(self):
        """
        Test whether adding or deleting lesson plan will affect the page
        """
        for i in range(0, 10):
            sample_text = "test_text_" + str(random.randint(0, 1000000))
            sample_author = "test_author_" + str(random.randint(0, 1000000))
            sample_grade_level = "test_grade_" + str(random.randint(0, 10000000))
            sample_course = "test_course_" + str(random.randint(100000, 1000000))
            sample_key_words = "test_keywords" + str(random.randint(100000, 1000000))
            sample_order = str(random.randint(40, 100))
            sample_abstract = "test_abstract_" + str(random.randint(0, 10000000))
            
            new_lessonplan = LessonPlan.objects.create(text=sample_text, author=sample_author, grade_level=sample_grade_level,
                    course=sample_course, key_words=sample_key_words, order=sample_order, abstract=sample_abstract)
            
            # Check if the response contains the lesson plan
            response = self.client.get(reverse('education:lesson-plans'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, new_lessonplan.text)
            self.assertContains(response, new_lessonplan.author)
            self.assertContains(response, new_lessonplan.grade_level)
            self.assertContains(response, new_lessonplan.course)
            self.assertContains(response, new_lessonplan.key_words)
            
            new_lessonplan.delete()
            # Check if the response does not contain the lesson plan just deleted
            response = self.client.get(reverse('education:lesson-plans'))
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, new_lessonplan.text)
            self.assertNotContains(response, new_lessonplan.author)
            self.assertNotContains(response, new_lessonplan.grade_level)
            self.assertNotContains(response, new_lessonplan.course)
            self.assertNotContains(response, new_lessonplan.key_words)
            
    def test_adding_multiple_lessonplans(self):
        """
        Test adding multiple lesson plans to the page
        and count whether they are added
        """
         # Check number of objects
        initial_count = LessonPlan.objects.count()
        for i in range(0, 10):
            sample_text = "test_text_" + str(random.randint(0, 1000000))
            sample_author = "test_author_" + str(random.randint(0, 1000000))
            sample_grade_level = "test_grade_" + str(random.randint(0, 10000000))
            sample_course = "test_course_" + str(random.randint(100000, 1000000))
            sample_key_words = "test_keywords" + str(random.randint(100000, 1000000))
            sample_order = str(random.randint(40, 100))
            sample_abstract = "test_abstract_" + str(random.randint(0, 10000000))
            
            new_lessonplan = LessonPlan.objects.create(text=sample_text, author=sample_author, grade_level=sample_grade_level,
                    course=sample_course, key_words=sample_key_words, order=sample_order, abstract=sample_abstract)
            
            # Check if the response contains the lesson plan
            response = self.client.get(reverse('education:lesson-plans'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, new_lessonplan.text)
            self.assertContains(response, new_lessonplan.author)
            self.assertContains(response, new_lessonplan.grade_level)
            self.assertContains(response, new_lessonplan.course)
            self.assertContains(response, new_lessonplan.key_words)
        self.assertEqual(LessonPlan.objects.count(), initial_count+ 10)
        
@override_settings(LANGUAGE_CODE='en')    
class TestLessonStandard(TestCase):
    """
    Simple test on a subset of the lesson plan data
    """
    fixtures = ['help_lessonplan_data_part1.json']
    def test_adding_standard(self):
        """
        Test simple rendering of the page
        """
        std_item_text = "test_text_" + str(random.randint(0, 1000000))
        std_item_type = LessonStandardType.objects.order_by('?')[0]
        std_item_lesson = LessonPlan.objects.order_by('?')[0]
        
        # Generate a random Lesson Standard
        std_item = LessonStandard.objects.create(text=std_item_text, type=std_item_type,lesson=std_item_lesson)
        
        response = self.client.get(reverse('education:lesson-plans'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, std_item_text)
        
        textList = []
        for i in range(0, 10):
            std_item_text = "test_text_" + str(random.randint(0, 1000000))
            std_item_type = LessonStandardType.objects.order_by('?')[0]
            std_item_lesson = LessonPlan.objects.order_by('?')[0]
            textList.append(std_item_text)
            
            # Generate a random Lesson Standard
            std_item = LessonStandard.objects.create(text=std_item_text, type=std_item_type,lesson=std_item_lesson)
        
        response = self.client.get(reverse('education:lesson-plans'))
        self.assertEqual(response.status_code, 200)
        for text_item in textList:
            self.assertContains(response, text_item)