
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from .models import *
import random

@override_settings(LANGUAGE_CODE='en')    
class TestTestLessonPlansNoData(TestCase):
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
class TestLessonPlans(TestCase):
    """
    Simple test on a subset of the lesson plan data
    """
    fixtures = ['help_lessonplan_data_part1.json']

    def test_lessons(self):
        """
        Test whether words really appears on the page
        """
        response = self.client.get(reverse('education:lesson-plans'))
        self.assertEqual(response.status_code, 200)
        for lessonplan_item in LessonPlan.objects.all():
            self.assertContains(response, lessonplan_item.text)
            self.assertContains(response, lessonplan_item.author)
            self.assertContains(response, lessonplan_item.grade_level)
            self.assertContains(response, lessonplan_item.course)
            self.assertContains(response, lessonplan_item.key_words)
