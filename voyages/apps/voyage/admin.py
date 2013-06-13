from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm
from django import forms

class MyFlatAdminForm(FlatpageForm):
    template2 = forms.CharField()

class FlatPageAdmin(FlatPageAdminOld):
    """Class serves flat pages module"""
 
    list_display = ['title', 'url']
  
    # prevents deleting of flat page
    actions = None

    # Prevents anyone from trying to add a new flat page
    def has_add_permission(self, request):
        return False

    class Media:
        js = ( 'scripts/tiny_mce/tinymce.min.js',
              'scripts/tiny_mce/textareas.js',
              )

# We have to unregister it, and then reregister
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

