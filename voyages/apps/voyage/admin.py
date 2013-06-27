from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
import autocomplete_light
from .forms import *
from .models import *


class FlatPageAdmin(admin.ModelAdmin):
    """
    Support for flat page.
    """
    fields = ('url', 'title', 'content')
    readonly_fields = ('url', 'title',)
    
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


class VoyageCaptainConnectionInline(admin.TabularInline):
    """
    Inline model for Captain Connection.
    """
    form = VoyageCaptainConnectionForm
    model = VoyageCaptainConnection
    extra = 3


class VoyageAdmin(admin.ModelAdmin):
    """
    Admin panel for Voyage class.
    It contains inlines elements and form for autocompleting as typing.
    """
    inlines = (VoyageCaptainConnectionInline,)
    form = autocomplete_light.modelform_factory(Voyage)

# class VoyageShipNationalityAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         """
#         Return empty perms dict thus hiding the model from admin index.
#         """
#         return {}

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Voyage, VoyageAdmin)
admin.site.register(VoyageGroupings)
admin.site.register(VoyageCaptain)
admin.site.register(VoyageShip)
admin.site.register(VoyageOutcome)
admin.site.register(VoyageItinerary)
admin.site.register(VoyageDates)
admin.site.register(VoyageCrew)
admin.site.register(VoyageSlavesCharacteristics)
admin.site.register(VoyageSources)
admin.site.register(Region)
admin.site.register(BroadRegion)
admin.site.register(Place)
