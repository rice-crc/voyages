import datetime
from haystack import indexes
from .models import *


class FaqIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    faq_question = indexes.CharField(model_attr='question')
    faq_answer = indexes.CharField(model_attr='answer')
    faq_question_order = indexes.IntegerField(model_attr='question_order')
    faq_category_desc = indexes.CharField()
    faq_category_order = indexes.IntegerField()

    def get_model(self):
        return Faq

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    def prepare_faq_category_order(self, obj):
        return obj.category.type_order
    def prepare_faq_category_desc(self, obj):
        return obj.category.text
    

class GlossaryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    glossary_term = indexes.CharField(model_attr='term')
    glossary_description = indexes.CharField(model_attr='description')

    def get_model(self):
        return Glossary

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
