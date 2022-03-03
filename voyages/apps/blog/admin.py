from django.contrib import admin
from django.db import models
from .models import Post

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
  
admin.site.register(Post, PostAdmin)