from django.contrib import admin
from .models import *
from .forms import *

class ImageAdmin(admin.ModelAdmin):
    list_filter = ['category']
    list_display = ['ready_to_go', 'title', 'file' ]
    list_display_links = ['title']
    list_editable = ['ready_to_go']
    search_fields = ['title', 'description']
    exclude = ['voyage']

    form = ImageAdminForm

    class Meta:
        model = Image


class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = ['visible_on_website', 'label', 'value']
    list_display_links = ['label']
    list_editable =  ['visible_on_website']
    ordering = ['value']
    search_fields = ['value']

    class Meta:
        model = ImageCategory


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageCategory, ImageCategoryAdmin)
