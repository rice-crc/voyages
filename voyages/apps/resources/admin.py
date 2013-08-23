from django.contrib import admin
from .models import *
from .forms import *

class ImageAdmin(admin.ModelAdmin):
    list_filter = ['category']
    list_display = ['image_id', 'file', 'title' ]
<<<<<<< HEAD
    #exclude = ['voyage']
=======
    exclude = ['voyage']
>>>>>>> 71b21db14a517bd0493bd72d5b7cbaba66c29754
    form = ImageAdminForm

    class Meta:
        model = Image


class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = ['value', 'label']

    class Meta:
        model = ImageCategory


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageCategory, ImageCategoryAdmin)
