import datetime
from haystack import indexes
from voyages.apps.help.models import *


class FaqIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    question = indexes.CharField(model_attr='question')
    answer = indexes.CharField(model_attr='answer')
    question_order = indexes.IntegerField(model_attr='question_order')

    def get_model(self):
        return Faq

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()