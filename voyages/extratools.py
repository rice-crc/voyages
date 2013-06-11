from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from haystack.forms import HighlightedSearchForm
from haystack.utils import Highlighter
     
class AdvancedEditor(forms.Textarea):
    class Media:
      js = ('scripts/tiny_mce/tinymce.min.js', 'scripts/tiny_mce/textareas_small.js',)
     
    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        self.attrs = {'class': 'advancededitor'}
        if attrs: self.attrs.update(attrs)
        super(AdvancedEditor, self).__init__(attrs)
     
    def render(self, name, value, attrs=None):
       rendered = super(AdvancedEditor, self).render(name, value, attrs)
       return rendered 

class FaqSearchForm(HighlightedSearchForm):
    """
    Use to search terms in FAQ section
    """
    #q = forms.CharField(required=True)
    #search_field = forms.CharField(label="")
    
    def search(self):
        sqs = super(HighlightedSearchForm)
        return sqs

class TextHighlighter(Highlighter):
    def highlight(self, text_block):
        self.text_block = text_block
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)

        start_offset = 0
        end_offset = len(text_block)
        return self.render_html(highlight_locations, start_offset, end_offset)

