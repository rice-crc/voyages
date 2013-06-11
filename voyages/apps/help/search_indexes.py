import datetime
from haystack import indexes
from .models import *


class FaqIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='mid', document=True, use_template=True)
    question = indexes.CharField(model_attr='question')
    answer = indexes.CharField(model_attr='answer')
    # define addition field
    #category = indexes.CharField(model_attr='category', indexed=False)

    def get_model(self):
        return Faq

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    def prepare_categoryText(self, obj):
        return obj.category.text
    
class FaqCategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    type_order = indexes.CharField(model_attr='type_order')
    text_desc = indexes.CharField(model_attr='text')

    def get_model(self):
        return FaqCategory

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class GlossaryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    term = indexes.CharField(model_attr='term')
    description = indexes.CharField(model_attr='description')

    def get_model(self):
        return Glossary

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
