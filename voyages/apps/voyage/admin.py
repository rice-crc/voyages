from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
import autocomplete_light
from .forms import *


# FlatPage Admin
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


# Voyage Admin
class VoyageShipInline(admin.StackedInline):
    form = VoyageShipForm
    model = VoyageShip
    extra = 1
    max_num = 1
    #inlines = (VoyageOwnerConnectionInline,)
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class VoyageCaptainConnectionInline(admin.TabularInline):
    """
    Inline model for Captain Connection.
    """
    form = VoyageCaptainConnectionForm
    model = VoyageCaptainConnection
    extra = 3


class VoyageShipOwnerInline(admin.TabularInline):
    """
    Inline model for Captain Connection.
    """
    form = VoyageShipOwnerConnectionForm
    model = VoyageShipOwnerConnection
    extra = 3


class VoyageCaptainAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class VoyageAdmin(admin.ModelAdmin):
    """
    Admin panel for Voyage class.
    It contains inlines elements and form for autocompleting as typing.
    """
    inlines = (VoyageCaptainConnectionInline, VoyageShipInline,
               VoyageShipOwnerInline)
    form = autocomplete_light.modelform_factory(Voyage)
    ordering = ['voyage_in_cd_rom', 'voyage_groupings']


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)


admin.site.register(VoyageGroupings)
admin.site.register(VoyageCaptain, VoyageCaptainAdmin)
admin.site.register(VoyageShipOwner)
#admin.site.register(VoyageShip, VoyageShipAdmin)
admin.site.register(VoyageOutcome)
admin.site.register(VoyageItinerary)
admin.site.register(VoyageDates)
admin.site.register(VoyageCrew)
admin.site.register(VoyageSlavesCharacteristics)
admin.site.register(VoyageSources)
admin.site.register(Region)
admin.site.register(BroadRegion)
admin.site.register(Place)
admin.site.register(VoyageShip.Nationality)
admin.site.register(VoyageShip.TonType)
admin.site.register(VoyageShip.RigOfVessel)
admin.site.register(Voyage, VoyageAdmin)
