from django.contrib import admin
from .models import *

class ImageAdmin(admin.ModelAdmin):
    list_filter = ['category']
    list_display = ['id', 'file', 'title']

    class Meta:
        model = Image


class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

    class Meta:
        model = ImageCategory


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageCategory, ImageCategoryAdmin)