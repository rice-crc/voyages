from django.contrib import admin
from django.db import models
from .models import Post
from .models import Tag
from .models import Institution
from .models import Author

from voyages.extratools import AdvancedEditor

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = {
        models.TextField: {'widget': AdvancedEditor(
        attrs={'class': 'tinymcetextarea'})}
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