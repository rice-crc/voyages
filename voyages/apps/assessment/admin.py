from django.contrib import admin
from .models import *


class ExportAreaAdmin(admin.ModelAdmin):
    fields = ["area_id", "name", "order_num", "latitude", "longitude",
              "show_at_zoom", "show_on_map"]

    list_display = ["area_id", "name", "order_num", "latitude", "longitude",
                    "show_at_zoom", "show_on_map"]


class ExportRegionAdmin(admin.ModelAdmin):
    fields = ["region_id", "name", "order_num", "latitude", "longitude",
              "show_at_zoom", "export_area", "show_on_map"]
    list_display = ["region_id", "name", "order_num", "latitude", "longitude",
                    "show_at_zoom", "export_area", "show_on_map"]


class ImportAreaAdmin(admin.ModelAdmin):
    fields = ["area_id", "name", "order_num", "latitude", "longitude",
              "show_at_zoom", "show_on_map"]
    list_display = ["area_id", "name", "order_num", "latitude", "longitude",
                    "show_at_zoom", "show_on_map"]


class ImportRegionAdmin(admin.ModelAdmin):
    fields = ["region_id", "name", "order_num", "latitude", "longitude",
              "show_at_zoom", "import_area", "show_on_map"]
    list_display = ["region_id", "name", "order_num", "latitude", "longitude",
                    "show_at_zoom", "import_area", "show_on_map"]


class NationAdmin(admin.ModelAdmin):
    fields = ["nation_id", "name", "order_num"]
    list_display = ["nation_id", "name", "order_num"]


class EstimateAdmin(admin.ModelAdmin):
    fields = ["estimate_id", "year", "nation", "embarkation_region", "disembarkation_region",
              "embarked_slaves", "disembarked_slaves"]


admin.site.register(ExportArea, ExportAreaAdmin)
admin.site.register(ExportRegion, ExportRegionAdmin)
admin.site.register(ImportArea, ImportAreaAdmin)
admin.site.register(ImportRegion, ImportRegionAdmin)
admin.site.register(Nation, NationAdmin)
admin.site.register(Estimate, EstimateAdmin)