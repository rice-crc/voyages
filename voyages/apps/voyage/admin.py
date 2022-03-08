from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _
from autocomplete_light import shortcuts as autocomplete_light

from .forms import (VoyageCaptainConnectionForm, VoyageCrewForm,
                    VoyageDatesForm, VoyageItineraryForm, VoyageOutcomeForm,
                    VoyageShipForm, VoyageShipOwnerConnectionForm,
                    VoyageSlavesNumbersForm, VoyageSourcesConnectionForm,
                    VoyagesSourcesAdminForm)
from .models import (BroadRegion, Nationality, OwnerOutcome, ParticularOutcome,
                     Place, Region, RigOfVessel, SlavesOutcome, TonType,
                     VesselCapturedOutcome, Voyage, VoyageCaptainConnection,
                     VoyageCrew, VoyageDates, VoyageGroupings, VoyageItinerary,
                     VoyageOutcome, VoyageShip, VoyageShipOwnerConnection,
                     VoyageSlavesNumbers, VoyageSources,
                     VoyageSourcesConnection, VoyageSourcesType)


# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'registration_required',
                'template_name',
            ),
        }),
    )

    class Media:
        js = (
            'scripts/tiny_mce/tinymce.min.js',
            'scripts/tiny_mce/textareas.js',
        )


# Voyage Admin
# Regions, Places
class BroadRegionAdmin(admin.ModelAdmin):
    list_display = ('broad_region', 'value', 'show_on_map')
    list_display_links = ('broad_region',)
    search_fields = ['broad_region', 'value']
    list_editable = ['show_on_map']


class RegionAdmin(admin.ModelAdmin):
    list_display = ('region', 'value', 'broad_region', 'show_on_map',
                    'show_on_main_map')
    list_display_links = ('region',)
    search_fields = ['region', 'value']
    list_editable = ['show_on_map', 'show_on_main_map']


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('place', 'value', 'region', 'longitude', 'latitude',
                    'show_on_main_map', 'show_on_voyage_map')
    list_display_links = ('place',)
    search_fields = ['place', 'value']
    ordering = ['value']
    list_editable = ['show_on_main_map', 'show_on_voyage_map']


# Technical
class VoyageGroupingsAdmin(admin.ModelAdmin):
    """
    Admin for VoyageGroupings
    """
    list_display = ['label', 'value']
    list_display_links = ['label']
    ordering = ['value']
    search_fields = ['label', 'value']


# Ship, Nation, Owners
class VoyageShipInline(admin.StackedInline):
    form = VoyageShipForm
    model = VoyageShip
    extra = 1
    max_num = 1

    def get_model_perms(self, _):
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
    # def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}


class VoyageNationalityAdmin(admin.ModelAdmin):
    """
    Admin for Voyage.Nationality
    """
    list_display = ('label', 'value')
    list_display_links = ('label',)
    search_fields = ['label', 'value']
    ordering = ['value']


class VoyageRigOfVesselAdmin(admin.ModelAdmin):
    """
    Admin for Voyage.RigOfVessel
    """
    list_display = ('label', 'value')
    list_display_links = ('label',)
    search_fields = ['label', 'value']
    ordering = ['value']


class VoyageTonTypeAdmin(admin.ModelAdmin):
    """
    Admin for Voyage.TonType
    """
    list_display = ('label', 'value')
    list_display_links = ('label',)
    search_fields = ['label', 'value']


# Voyage Outcome
class VoyageOutcomeInline(admin.TabularInline):
    form = VoyageOutcomeForm
    model = VoyageOutcome
    extra = 1
    max_num = 1

    def get_model_perms(self, _):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class VoyageParticularOutcomeAdmin(admin.ModelAdmin):
    """
    Admin for VoyageOutcome.ParticularOutcome
    """
    list_display = ['label', 'value']
    list_display_links = ['label']
    ordering = ['value']
    search_fields = ['label', 'value']


class VoyageSlavesOutcomeAdmin(admin.ModelAdmin):
    """
    Admin for VoyageOutcome.SlavesOutcome
    """
    list_display = ('label', 'value')
    list_display_links = ('label',)
    ordering = ['value']
    search_fields = ['label', 'value']


class VoyageVesselOutcomeAdmin(admin.ModelAdmin):
    """
    Admin for VoyageOutcome.VesselCapturedOutcome
    """
    list_display = ('label', 'value')
    list_display_links = ('label',)
    search_fields = ['label', 'value']


# Voyage Itinerary
class VoyageItineraryInline(admin.StackedInline):
    form = VoyageItineraryForm
    model = VoyageItinerary
    extra = 1
    max_num = 1

    def get_model_perms(self, _):
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

    def get_model_perms(self, _):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


# Voyage Captain and Crew
class VoyageCaptainAdmin(admin.ModelAdmin):
    fields = ('name',)
    # def get_model_perms(self, request):
    #    """
    #    Return empty perms dict thus hiding the model from admin index.
    #    """
    #    return {}


class VoyageCaptainConnectionAdmin(admin.ModelAdmin):
    """
    Admin for VoyageOutcome.VesselCapturedOutcome
    """
    list_display = (
        'voyage',
        'captain_order',
        'captain',
    )
    # def get_model_perms(self, request):
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

    def get_model_perms(self, _):
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

    def get_model_perms(self, _):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


# Voyage Sources


class VoyageSourcesAdmin(admin.ModelAdmin):
    """
    Admin for VoyageSources.
    """
    list_display = (
        'short_ref',
        'source_type',
        'full_ref',
    )
    search_fields = ('short_ref', 'full_ref')
    list_filter = ['source_type']
    list_per_page = 10000000  # no pages
    form = VoyagesSourcesAdminForm


class VoyageSourcesTypeAdmin(admin.ModelAdmin):
    """
    Admin for VoyageSourcesType.
    """
    list_display = ['group_name', 'group_id']
    search_fields = ['group_name']


class VoyageSourcesConnectionInline(admin.TabularInline):
    """
    Inline model for Captain Connection.
    """
    form = VoyageSourcesConnectionForm
    model = VoyageSourcesConnection
    extra = 5
    max_num = 18


class OwnerOutcomesAdmin(admin.ModelAdmin):
    list_display = ('label', 'value')
    list_display_links = ('label',)
    search_fields = ['label', 'value']
    ordering = ['value']


# Voyage (main section)
class VoyageAdmin(admin.ModelAdmin):
    """
    Admin panel for Voyage class.
    It contains inlines elements and form for autocompleting as typing.
    """
    inlines = (VoyageCaptainConnectionInline, VoyageShipInline,
               VoyageShipOwnerInline, VoyageOutcomeInline,
               VoyageItineraryInline, VoyageDatesInline, VoyageCrewInline,
               VoyageSlavesNumbersInline, VoyageSourcesConnectionInline)
    form = autocomplete_light.modelform_factory(Voyage, fields='__all__')
    list_display = ['voyage_id']
    list_display_links = ['voyage_id']
    ordering = ['-voyage_in_cd_rom', 'voyage_groupings', 'voyage_id']
    search_fields = ['voyage_id']
    exclude = ('voyage_ship', 'voyage_itinerary', 'voyage_dates',
               'voyage_crew', 'voyage_slaves_numbers')

    class Meta:
        fields = '__all__'


# Re-register FlatPageAdmin
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
# admin.site.register(VoyageShipOwner, VoyageShipOwnerAdmin)
admin.site.register(Nationality, VoyageNationalityAdmin)
admin.site.register(TonType, VoyageTonTypeAdmin)
admin.site.register(RigOfVessel, VoyageRigOfVesselAdmin)

# Voyage Outcome
admin.site.register(OwnerOutcome, OwnerOutcomesAdmin)
admin.site.register(ParticularOutcome, VoyageParticularOutcomeAdmin)
admin.site.register(SlavesOutcome, VoyageSlavesOutcomeAdmin)
admin.site.register(VesselCapturedOutcome, VoyageVesselOutcomeAdmin)
# attached as inline in Voyage section

# Voyage Slaves (characteristics)
# attached as inline in Voyage section

# Voyage Sources
admin.site.register(VoyageSources, VoyageSourcesAdmin)
admin.site.register(VoyageSourcesType, VoyageSourcesTypeAdmin)

# Voyage (main section)
admin.site.register(Voyage, VoyageAdmin)
