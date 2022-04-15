from django.contrib import admin
from django.db import models
from django import forms

from django.conf import settings

from .models import Post
from .models import Tag
from .models import Institution
from .models import Author

from voyages.extratools import AdvancedEditor


class AdvancedEditorManager(forms.Textarea):

    class Media:
        js = (
            '//cdn.tiny.cloud/1/evau54786a4pxb62mp84sjc26h72hrpdu9b5'
            'ht3zzn8oisd5/tinymce/5/tinymce.min.js',
            'scripts/filebrowser/TinyMCEv5Admin.js')

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        self.attrs = {'class': 'advancededitormanager'}
        if attrs:
            self.attrs.update(attrs)
        super().__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super().render(name, value, attrs)
        return rendered

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    
    formfield_overrides = {
        models.TextField: {'widget': AdvancedEditorManager(
        attrs={'class': 'tinymcetextareamanager'})}
    }

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class InstitutionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Post, PostAdmin)

admin.site.register(Tag,TagAdmin)

admin.site.register(Institution,InstitutionAdmin)

admin.site.register(Author,AuthorAdmin)


