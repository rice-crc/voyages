from haystack import indexes
from .models import *
from voyages.apps.voyage.search_indexes import TranslatedTextField
from django.utils import translation
from django.utils.translation import ugettext as _

def get_translation(text, lang):
    with translation.override(lang):
        return _(text)

class FaqIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    faq_question = indexes.CharField(model_attr='question')
    faq_question_lang_en = TranslatedTextField(null=True, unidecode=False, model_attr='question')
    faq_question_lang_pt = TranslatedTextField(null=True, unidecode=False, model_attr='question')
    faq_answer = indexes.CharField(model_attr='answer')
    faq_answer_lang_en = TranslatedTextField(null=True, unidecode=False, model_attr='answer')
    faq_answer_lang_pt = TranslatedTextField(null=True, unidecode=False, model_attr='answer')
    faq_question_order = indexes.IntegerField(model_attr='question_order')
    faq_category_order = indexes.IntegerField(model_attr='category__type_order')
    faq_category_desc = indexes.CharField(model_attr='category__text')
    faq_category_desc_lang_en = TranslatedTextField(null=True, unidecode=False, model_attr='category__text')
    faq_category_desc_lang_pt = TranslatedTextField(null=True, unidecode=False, model_attr='category__text')

    def get_model(self):
        return Faq

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    # Manually define full text index so that the text can be searched in translated languages.
    def prepare_text(self, obj):
        return ' '.join([obj.question, obj.answer, get_translation(obj.question, 'pt'), get_translation(obj.answer, 'pt')])


class GlossaryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    glossary_term = indexes.CharField(faceted=True, model_attr='term')
    glossary_term_lang_en = TranslatedTextField(null=True, unidecode=False, model_attr='term')
    glossary_term_lang_pt = TranslatedTextField(null=True, unidecode=False, model_attr='term')
    glossary_description = indexes.CharField(model_attr='description')
    glossary_description_lang_en = TranslatedTextField(null=True, unidecode=False, model_attr='description')
    glossary_description_lang_pt = TranslatedTextField(null=True, unidecode=False, model_attr='description')

    def get_model(self):
        return Glossary

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    # Manually define full text index so that the text can be searched in translated languages.
    def prepare_text(self, obj):
        return ' '.join([obj.term, obj.description, get_translation(obj.term, 'pt'), get_translation(obj.description, 'pt')])
