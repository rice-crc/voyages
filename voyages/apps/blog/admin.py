from django.contrib import admin
from django.db import models
from django import forms

from django.conf import settings

from django.conf.urls import url

from django.template.response import TemplateResponse

from .models import Post
from .models import Tag
from .models import Institution
from .models import Author


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
    list_display = ('title', 'slug', 'language', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    
    formfield_overrides = {
        models.TextField: {'widget': AdvancedEditorManager(
        attrs={'class': 'tinymcetextareamanager'})}
    }

    def get_urls(self):
        urls = super(PostAdmin, self).get_urls()

        security_urls = [
            url(r'^newsmigration/$', self.admin_site.admin_view(self.news_migration))            
        ]

        print(urls)
        return security_urls + urls

    def news_migration (self, request):
        context = dict(
            self.admin_site.each_context(request), # Include common variables for rendering the admin template.
            something="test",
        )
        return TemplateResponse(request, "blog/news-migration.html", context)


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

