from __future__ import unicode_literals

from builtins import object

from django import forms
from django.conf import settings
from haystack.utils import Highlighter


class AdvancedEditor(forms.Textarea):

    class Media(object):
        js = (
            '//cdn.tiny.cloud/1/evau54786a4pxb62mp84sjc26h72hrpdu9b5ht3zzn8oisd5/tinymce/5/tinymce.min.js',
            'scripts/tiny_mce/textareas_small.js')

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        self.attrs = {'class': 'advancededitor'}
        if attrs:
            self.attrs.update(attrs)
        super(AdvancedEditor, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(AdvancedEditor, self).render(name, value, attrs)
        return rendered


class TextHighlighter(Highlighter):

    def highlight(self, text_block):
        self.text_block = text_block
        highlight_locations = self.find_highlightable_words()
        # start_offset, end_offset = self.find_window(highlight_locations)

        start_offset = 0
        end_offset = len(text_block)
        return self.render_html(highlight_locations, start_offset, end_offset)
