# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
import haystack
from voyages.apps.help.models import Glossary, Faq, FaqCategory
import mock


class TestGlossarySearch(TestCase):
    """
    """
    fixtures = ['glossary.json']


class TestFaqSearch(TestCase):
    """
    """
    fixtures = ['faq_data_all.json']