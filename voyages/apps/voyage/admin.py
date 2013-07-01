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

# Technical
class VoyageGroupingsAdmin(admin.ModelAdmin):
    """
    Admin for VoyageGroupings
    """
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


# Ship, Nation, Owners
class VoyageShipInline(admin.TabularInline):
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
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class VoyageNationalityAdmin(admin.ModelAdmin):
    """
    Admin for Voyage.Nationality
    """
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class VoyageRigOfVesselAdmin(admin.ModelAdmin):
    """
    Admin for Voyage.RigOfVessel
    """
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class VoyageTonTypeAdmin(admin.ModelAdmin):
    """
    Admin for Voyage.TonType
    """
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


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
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class VoyageSourcesAdmin(admin.ModelAdmin):
    """
    Admin for VoyageSources.
    """
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class VoyageSourcesConnectionInline(admin.TabularInline):
    """
    Inline model for Captain Connection.
    """
    form = VoyageSourcesConnectionForm
    model = VoyageSourcesConnection
    extra = 15

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
    ordering = ['voyage_in_cd_rom', 'voyage_groupings']


# Registers section
# Flat Page
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

# Voyage
# Regions, Places
admin.site.register(Region)
admin.site.register(BroadRegion)
admin.site.register(Place)

# Technical
admin.site.register(VoyageGroupings, VoyageGroupingsAdmin)

# Ship, Nation, Owners
admin.site.register(VoyageShipOwner, VoyageShipOwnerAdmin)
admin.site.register(VoyageShip.Nationality, VoyageNationalityAdmin)
admin.site.register(VoyageShip.TonType, VoyageTonTypeAdmin)
admin.site.register(VoyageShip.RigOfVessel, VoyageRigOfVesselAdmin)
#admin.site.register(VoyageShip, VoyageShipAdmin)

# Voyage Outcome
# attached as inline in Voyage section

# Voyage Itinerary
# attached as inline in Voyage section

# Voyage Dates
# attached as inline in Voyage section

# Voyage Captain and Crew
# Crew attached as inline in Voyage section
admin.site.register(VoyageCaptain, VoyageCaptainAdmin)

# Voyage Slaves (numbers)
# attached as inline in Voyage section

# Voyage Slaves (characteristics)
# attached as inline in Voyage section

# Voyage Sources
admin.site.register(VoyageSources, VoyageSourcesAdmin)

# Voyage (main section)
admin.site.register(Voyage, VoyageAdmin)
