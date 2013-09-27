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
# Regions, Places
class BroadRegionAdmin(admin.ModelAdmin):
    list_display = ('value', 'broad_region')
    list_display_links = ('broad_region',)
    search_fields = ['value', 'broad_region']

class RegionAdmin(admin.ModelAdmin):
    list_display = ('value', 'region')
    list_display_links = ('region',)
    search_fields = ['value', 'region']


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('value', 'place')
    list_display_links = ('place',)
    search_fields = ['value', 'place']


# Technical
class VoyageGroupingsAdmin(admin.ModelAdmin):
    """
    Admin for VoyageGroupings
    """
    #def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}


# Ship, Nation, Owners
class VoyageShipInline(admin.StackedInline):
    form = VoyageShipForm
    model = VoyageShip
    extra = 1
    max_num = 1
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class VoyageShipOwnerInline(admin.TabularInline):
    """
    Inline model for Captain Connection.
    """
    form = VoyageShipOwnerConnectionForm
    model = VoyageShipOwnerConnection
    extra = 3


class VoyageShipOwnerAdmin(admin.ModelAdmin):
    """
    Admin for VoyageShipOwner.
    """
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ['name']
    #def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}


class VoyageNationalityAdmin(admin.ModelAdmin):
    """
    Admin for Voyage.Nationality
    """
    list_display = ('value', 'label')
    list_display_links = ('label',)
    search_fields = ['value', 'label']
    #def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}


class VoyageRigOfVesselAdmin(admin.ModelAdmin):
    """
    Admin for Voyage.RigOfVessel
    """
    list_display = ('value', 'label')
    list_display_links = ('label',)
    search_fields = ['value', 'label']
    #def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}


class VoyageTonTypeAdmin(admin.ModelAdmin):
    """
    Admin for Voyage.TonType
    """
    list_display = ('value', 'label')
    list_display_links = ('label',)
    search_fields = ['value', 'label']
    #def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}


# Voyage Outcome
class VoyageOutcomeInline(admin.TabularInline):
    form = VoyageOutcomeForm
    model = VoyageOutcome
    extra = 1
    max_num = 1

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class VoyageParticularOutcomeAdmin(admin.ModelAdmin):
    """
    Admin for VoyageOutcome.ParticularOutcome
    """
    list_display = ('value', 'label')
    list_display_links = ('label',)
    #def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}


class VoyageSlavesOutcomeAdmin(admin.ModelAdmin):
    """
    Admin for VoyageOutcome.SlavesOutcome
    """
    list_display = ('value', 'label')
    list_display_links = ('label',)
    #def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}

class VoyageVesselOutcomeAdmin(admin.ModelAdmin):
    """
    Admin for VoyageOutcome.VesselCapturedOutcome
    """
    list_display = ('value', 'label')
    list_display_links = ('label',)
    #def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}

# Voyage Itinerary
class VoyageItineraryInline(admin.StackedInline):
    form = VoyageItineraryForm
    model = VoyageItinerary
    extra = 1
    max_num = 1

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


# Voyage Dates
class VoyageDatesInline(admin.StackedInline):
    form = VoyageDatesForm
    model = VoyageDates
    extra = 1
    max_num = 1

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


# Voyage Captain and Crew
class VoyageCaptainAdmin(admin.ModelAdmin):
    fields = ('name',)
    #def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}


class VoyageCaptainConnectionAdmin(admin.ModelAdmin):

    """
    Admin for VoyageOutcome.VesselCapturedOutcome
    """
    list_display = ('voyage', 'captain_order', 'captain',)
    #def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}


class VoyageCaptainConnectionInline(admin.TabularInline):
    """
    Inline model for Captain Connection.
    """
    form = VoyageCaptainConnectionForm
    model = VoyageCaptainConnection
    extra = 3


class VoyageCrewInline(admin.TabularInline):
    """
    Inline model for Captain Connection.
    """
    form = VoyageCrewForm
    model = VoyageCrew
    extra = 1
    max_num = 1

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


# Voyage Slaves (numbers + characteristics)
class VoyageSlavesNumbersInline(admin.StackedInline):
    """
    Inline model for Slave Characteristics.
    """
    form = VoyageSlavesNumbersForm
    model = VoyageSlavesNumbers
    extra = 1
    max_num = 1

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}



# Voyage Sources
class VoyageSourcesConnectionAdmin(admin.ModelAdmin):
    pass
    #def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}


class VoyageSourcesAdmin(admin.ModelAdmin):
    """
    Admin for VoyageSources.
    """
    list_display = ('short_ref', 'full_ref')
    search_fields = ('short_ref', 'full_ref')
    form = VoyagesSourcesAdminForm
    #def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}


class VoyageSourcesConnectionInline(admin.TabularInline):
    """
    Inline model for Captain Connection.
    """
    form = VoyageSourcesConnectionForm
    model = VoyageSourcesConnection
    extra = 5
    max_num = 18


# Voyage (main section)
class VoyageAdmin(admin.ModelAdmin):
    """
    Admin panel for Voyage class.
    It contains inlines elements and form for autocompleting as typing.
    """
    inlines = (VoyageCaptainConnectionInline, VoyageShipInline,
               VoyageShipOwnerInline, VoyageOutcomeInline,
               VoyageItineraryInline, VoyageDatesInline,
               VoyageCrewInline, VoyageSlavesNumbersInline,
               VoyageSourcesConnectionInline)
    form = autocomplete_light.modelform_factory(Voyage)
    list_display = ['voyage_in_cd_rom', 'voyage_groupings', 'voyage_id']
    list_display_links = ['voyage_id']
    ordering = ['-voyage_in_cd_rom', 'voyage_groupings', 'voyage_id']
    search_fields = ('voyage_id',)
    exclude = ('voyage_ship', 'voyage_itinerary', 'voyage_dates', 'voyage_crew', 'voyage_slaves_numbers')
    #list_display = ('voyage_id',)


# Registers section
# Flat Page
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

# Voyage
# Regions, Places
admin.site.register(Region, RegionAdmin)
admin.site.register(BroadRegion, BroadRegionAdmin)
admin.site.register(Place, PlaceAdmin)

# Technical
admin.site.register(VoyageGroupings, VoyageGroupingsAdmin)

# Ship, Nation, Owners
#admin.site.register(VoyageShipOwner, VoyageShipOwnerAdmin)
admin.site.register(Nationality, VoyageNationalityAdmin)
admin.site.register(TonType, VoyageTonTypeAdmin)
admin.site.register(RigOfVessel, VoyageRigOfVesselAdmin)
admin.site.register(VoyageShip)

# Voyage Outcome
admin.site.register(OwnerOutcome)
admin.site.register(ParticularOutcome, VoyageParticularOutcomeAdmin)
admin.site.register(SlavesOutcome, VoyageSlavesOutcomeAdmin)
admin.site.register(VesselCapturedOutcome, VoyageVesselOutcomeAdmin)
# attached as inline in Voyage section


# Voyage Slaves (characteristics)
# attached as inline in Voyage section

# Voyage Sources
admin.site.register(VoyageSources, VoyageSourcesAdmin)
admin.site.register(VoyageSourcesType)

# Voyage (main section)
admin.site.register(Voyage, VoyageAdmin)
