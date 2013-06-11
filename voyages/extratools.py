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


from django.utils.html import strip_tags
class TextHighlighter(Highlighter):
    def highlight(self, text_block):
        self.text_block = text_block
        highlight_locations = self.find_highlightable_words()
        #start_offset, end_offset = self.find_window(highlight_locations)

        start_offset = 0
        end_offset = len(text_block)
        return self.render_html(highlight_locations, start_offset, end_offset)

    def render_html(self, highlight_locations=None, start_offset=None, end_offset=None):
        # Start by chopping the block down to the proper window.
        text = self.text_block[start_offset:end_offset]
        
        # Invert highlight_locations to a location -> term list
        term_list = []
        
        for term, locations in highlight_locations.items():
            term_list += [(loc - start_offset, term) for loc in locations]
            
        loc_to_term = sorted(term_list)
        if term_list:
            3 / 0
        
        # Prepare the highlight template
        if self.css_class:
            hl_start = '<%s class="%s">' % (self.html_tag, self.css_class)
        else:
            hl_start = '<%s>' % (self.html_tag)
        
        hl_end = '</%s>' % self.html_tag
        highlight_length = len(hl_start + hl_end)
        
        # Copy the part from the start of the string to the first match,
        # and there replace the match with a highlighted version.
        highlighted_chunk = ""
        matched_so_far = 0
        prev = 0
        prev_str = ""
        
        for cur, cur_str in loc_to_term:
            # This can be in a different case than cur_str
            actual_term = text[cur:cur + len(cur_str)]
            
            # Handle incorrect highlight_locations by first checking for the term
            if actual_term.lower() == cur_str:
                highlighted_chunk += text[prev + len(prev_str):cur] + hl_start + actual_term + hl_end
                prev = cur
                prev_str = cur_str
                
                # Keep track of how far we've copied so far, for the last step
                matched_so_far = cur + len(actual_term)
        
        # Don't forget the chunk after the last term
        highlighted_chunk += text[matched_so_far:]
        
        if start_offset > 0:
            highlighted_chunk = '...%s' % highlighted_chunk
        
        if end_offset < len(self.text_block):
            highlighted_chunk = '%s...' % highlighted_chunk
        
        return highlighted_chunk