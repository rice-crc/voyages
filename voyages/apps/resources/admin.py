from django.contrib import admin
from .models import *
from .forms import *

class ImageAdmin(admin.ModelAdmin):
    list_filter = ['category']
    list_display = ['image_id', 'file', 'title' ]
<<<<<<< HEAD
=======
    #exclude = ['voyage']
>>>>>>> a3ae4af8fa81d4b9000b58bb1a5931b90a5612fb
    form = ImageAdminForm

    class Meta:
        model = Image


class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = ['value', 'label']

    class Meta:
        model = ImageCategory


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageCategory, ImageCategoryAdmin)
