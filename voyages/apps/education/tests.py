
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from .models import *

@override_settings(LANGUAGE_CODE='en')
class SimpleTestEducation(TestCase):
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
        Test for containment
        """
        listAllObjects = LessonPlan.objects.all()
        self.assertEqual(len(listAllObjects) > 0, True)
        
    def test_word_contains(self):
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
class TestContainment(TestCase):
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
        response = self.client.get(reverse('education:lesson-plans'))
        for lessonplan_item in LessonPlan.objects.all():
            self.assertContains(response, lessonplan_item.text)
            self.assertContains(response, lessonplan_item.author)
            self.assertContains(response, lessonplan_item.grade_level)
            self.assertContains(response, lessonplan_item.course)
            self.assertContains(response, lessonplan_item.key_words)
    
    def test_adding_new_lesson_plan(self):
        new_lessonplan_1 = LessonPlan.objects.create(text="12abc", author="AAAA Random author Test", grade_level="1000-2000",
                course='History 999', key_words='nokey;wqwertyyu', order=10, abstract='BBBB Empty Abstract')
        response = self.client.get(reverse('education:lesson-plans'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_lessonplan_1.text)
        self.assertContains(response, new_lessonplan_1.author)
        self.assertContains(response, new_lessonplan_1.grade_level)
        self.assertContains(response, new_lessonplan_1.course)
        self.assertContains(response, new_lessonplan_1.key_words)
        
        