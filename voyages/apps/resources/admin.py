from __future__ import unicode_literals

from django.contrib import admin

from .forms import ImageAdminForm
from .models import AfricanName, Country, Image, ImageCategory, SexAge


class ImageAdmin(admin.ModelAdmin):
    list_filter = ['category']
    list_display = ['ready_to_go', 'title', 'file']
    list_display_links = ['title']
    list_editable = ['ready_to_go']
    search_fields = ['title', 'description']
    exclude = ['voyage']

    form = ImageAdminForm

    class Meta:
        model = Image


class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = ['visible_on_website', 'label', 'value']
    list_display_links = ['label']
    list_editable = ['visible_on_website']
    ordering = ['value']
    search_fields = ['value']

    class Meta:
        model = ImageCategory


class CountryAdmin(admin.ModelAdmin):
    list_display = ['country_id', 'name']
    list_display_links = ['name']
    ordering = ['country_id']
    search_fields = ['country_id', 'name']

    class Meta:
        model = Country


class SexAgeAdmin(admin.ModelAdmin):
    list_display = ['sex_age_id', 'name']
    list_display_links = ['name']
    ordering = ['sex_age_id']
    search_fields = ['sex_age_id', 'name']

    class Meta:
        model = SexAge


class AfricanNameAdmin(admin.ModelAdmin):
    list_display = [
        'slave_id', 'name', 'age', 'height', 'source', 'ship_name',
        'date_arrived', 'voyage_number', 'sex_age', 'country',
        'disembarkation_port', 'embarkation_port'
    ]
    list_display_links = ['name', 'slave_id']
    exclude = [
        'voyage',
    ]
    ordering = ['slave_id']
    search_fields = [
        'slave_id', 'name', 'age', 'height', 'source', 'ship_name',
        'date_arrived', 'voyage_number'
    ]

    class Meta:
        model = AfricanName


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageCategory, ImageCategoryAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(SexAge, SexAgeAdmin)
admin.site.register(AfricanName, AfricanNameAdmin)
