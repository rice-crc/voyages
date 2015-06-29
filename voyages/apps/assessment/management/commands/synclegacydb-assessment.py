import traceback
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

class Command(BaseCommand):
    help = 'Synchronize the legacy db Estimates tables with the new Django modelled db'

    @transaction.commit_manually
    def handle(self, *args, **options):
        try:
            from voyages.apps.assessment import models
            from voyages.apps.voyage import legacy_models
            # Delete current records.
            models.ExportArea.objects.all().delete()
            models.ExportRegion.objects.all().delete()
            models.ImportArea.objects.all().delete()
            models.ImportRegion.objects.all().delete()
            models.Nation.objects.all().delete()
            models.Estimate.objects.all().delete()

            legacy_export_areas = legacy_models.EstimatesExportAreas.objects.all()
            export_areas = {}
            for legacy_export_area in legacy_export_areas:
                export_area = models.ExportArea()
                export_area.name = legacy_export_area.name
                export_area.order_num = legacy_export_area.order_num
                export_area.latitude = legacy_export_area.latitude
                export_area.longitude = legacy_export_area.longitude
                export_area.show_at_zoom = legacy_export_area.show_at_zoom
                export_area.show_on_map = legacy_export_area.show_on_map
                export_areas[legacy_export_area.id] = export_area
                export_area.save()

            legacy_export_regions = legacy_models.EstimatesExportRegions.objects.all()
            export_regions = {}
            for legacy_export_region in legacy_export_regions:
                export_region = models.ExportRegion()
                export_region.name = legacy_export_region.name
                export_region.order_num = legacy_export_region.order_num
                export_region.latitude = legacy_export_region.latitude
                export_region.longitude = legacy_export_region.longitude
                export_region.show_at_zoom = legacy_export_region.show_at_zoom
                export_region.show_on_map = legacy_export_region.show_on_map
                export_region.export_area = export_areas[legacy_export_region.area_id]
                export_regions[legacy_export_region.id] = export_region
                export_region.save()

            legacy_import_areas = legacy_models.EstimatesImportAreas.objects.all()
            import_areas = {}
            for legacy_import_area in legacy_import_areas:
                import_area = models.ImportArea()
                import_area.name = legacy_import_area.name
                import_area.order_num = legacy_import_area.order_num
                import_area.latitude = legacy_import_area.latitude
                import_area.longitude = legacy_import_area.longitude
                import_area.show_at_zoom = legacy_import_area.show_at_zoom
                import_area.show_on_map = legacy_import_area.show_on_map
                import_areas[legacy_import_area.id] = import_area
                import_area.save()

            legacy_import_regions = legacy_models.EstimatesImportRegions.objects.all()
            import_regions = {}
            for legacy_import_region in legacy_import_regions:
                import_region = models.ImportRegion()
                import_region.name = legacy_import_region.name
                import_region.order_num = legacy_import_region.order_num
                import_region.latitude = legacy_import_region.latitude
                import_region.longitude = legacy_import_region.longitude
                import_region.show_at_zoom = legacy_import_region.show_at_zoom
                import_region.show_on_map = legacy_import_region.show_on_map
                import_region.import_area = import_areas[legacy_import_region.area_id]
                import_regions[legacy_import_region.id] = import_region
                import_region.save()
            
            legacy_nations = legacy_models.Nations.objects.all()
            nations = {}
            for legacy_nation in legacy_nations:
                nation = models.Nation()
                nation.name = legacy_nation.name
                nation.order_num = legacy_nation.order_num
                nations[legacy_nation.id] = nation
                nation.save()

            legacy_estimates = legacy_models.Estimates.objects.all()
            for legacy_estimate in legacy_estimates:
                estimate = models.Estimate()
                estimate.year = legacy_estimate.yeardep
                estimate.disembarkation_region = import_regions[legacy_estimate.mjselimp_id]
                estimate.embarkation_region = export_regions[legacy_estimate.majbuyrg_id]
                estimate.disembarked_slaves = legacy_estimate.slamimp
                estimate.embarked_slaves = legacy_estimate.slaximp
                estimate.nation = nations[legacy_estimate.nation_id]
                estimate.save()
            transaction.commit()
            print "synclegacydb-assessment completed!"
        except Exception as ex:
            print "sorry!"
            traceback.print_exc()
