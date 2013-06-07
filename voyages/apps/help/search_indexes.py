import datetime
from haystack import indexes
from voyages.apps.help.models import FaqCategory, Faq


class FaqIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='mid', document=True, use_template=True)
    question = indexes.CharField(model_attr='question')
    answer = indexes.CharField(model_attr='answer')
    


    def get_model(self):
        return Faq

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()