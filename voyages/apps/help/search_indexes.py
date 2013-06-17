import datetime
from haystack import indexes
from .models import *


class FaqIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    faq_question = indexes.FacetMultiValueField()
    faq_answer = indexes.FacetMultiValueField()
    faq_question_order = indexes.IntegerField(model_attr='question_order')
    faq_category_desc = indexes.FacetMultiValueField()
    faq_category_order = indexes.IntegerField()

    def get_model(self):
        return Faq

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    
    def prepare_faq_question(self, obj):
        return obj.question
    
    def prepare_faq_answer(self, obj):
        return obj.answer
    
    def prepare_faq_category_order(self, obj):
        return obj.category.type_order
    
    def prepare_faq_category_desc(self, obj):
        return obj.category.text
    

class GlossaryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    glossary_term = indexes.FacetMultiValueField()
    glossary_description = indexes.FacetMultiValueField()

    def get_model(self):
        return Glossary

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_glossary_term(self, obj):
        return obj.term
    
    def prepare_glossary_description(self, obj):
        return obj.description