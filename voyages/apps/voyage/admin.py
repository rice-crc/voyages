from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld

class FlatPageAdmin(FlatPageAdminOld):
    list_display = ['title', 'url']
    readonly_fields= ['title', 'url']
    class Media:
        js = ( 'scripts/tiny_mce/tinymce.min.js',
              'scripts/tiny_mce/textareas.js',
              )

# We have to unregister it, and then reregister
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

