from __future__ import unicode_literals

from django.contrib import admin

from .models import (Estimate, ExportArea, ExportRegion, ImportArea,
                     ImportRegion, Nation)


class ExportAreaAdmin(admin.ModelAdmin):
    fields = [
        "name", "order_num", "latitude", "longitude", "show_at_zoom",
        "show_on_map"
    ]

    list_display = [
        "name", "order_num", "latitude", "longitude", "show_at_zoom",
        "show_on_map"
    ]


class ExportRegionAdmin(admin.ModelAdmin):
    fields = [
        "name", "order_num", "latitude", "longitude", "show_at_zoom",
        "export_area", "show_on_map"
    ]
    list_display = [
        "name", "order_num", "latitude", "longitude", "show_at_zoom",
        "export_area", "show_on_map"
    ]


class ImportAreaAdmin(admin.ModelAdmin):
    fields = [
        "name", "order_num", "latitude", "longitude", "show_at_zoom",
        "show_on_map"
    ]
    list_display = [
        "name", "order_num", "latitude", "longitude", "show_at_zoom",
        "show_on_map"
    ]


class ImportRegionAdmin(admin.ModelAdmin):
    fields = [
        "name", "order_num", "latitude", "longitude", "show_at_zoom",
        "import_area", "show_on_map"
    ]
    list_display = [
        "name", "order_num", "latitude", "longitude", "show_at_zoom",
        "import_area", "show_on_map"
    ]


class NationAdmin(admin.ModelAdmin):
    fields = ["name", "order_num"]
    list_display = ["name", "order_num"]


class EstimateAdmin(admin.ModelAdmin):
    fields = [
        "year", "nation", "embarkation_region", "disembarkation_region",
        "embarked_slaves", "disembarked_slaves"
    ]
    list_display = [
        "id", "year", "nation", "embarkation_region", "disembarkation_region",
        "embarked_slaves", "disembarked_slaves"
    ]


admin.site.register(ExportArea, ExportAreaAdmin)
admin.site.register(ExportRegion, ExportRegionAdmin)
admin.site.register(ImportArea, ImportAreaAdmin)
admin.site.register(ImportRegion, ImportRegionAdmin)
admin.site.register(Nation, NationAdmin)
admin.site.register(Estimate, EstimateAdmin)
