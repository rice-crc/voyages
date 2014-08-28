from haystack.query import SearchQuerySet
from .models import *


def get_flags():
    a = SearchQuerySet().models(Nation)
    nations = [(k.name, 1) for k in a]
    return [nations, ]


def get_broad_regions(area):
    areas_from_query = SearchQuerySet().models(area)
    areas = [(k.name, 1) for k in areas_from_query]
    print "areas = " + str(areas)

    return [areas, ]


def get_regions(region, area, mode="export"):
    return_areas = []
    return_regions = []
    areas = SearchQuerySet().models(area)

    # For each area, retrieve list of regions and add to the list with an appropriate length
    for local_area in areas:

        # Retrieve regions
        if mode == "export":
            local_regions = SearchQuerySet().models(region).filter(export_area__exact=local_area.name)
        else:
            local_regions = SearchQuerySet().models(region).filter(import_area__exact=local_area.name)

        if len(local_regions) == 0:
            continue
        # Add the area
        return_areas.append((local_area.name, len(local_regions)))

        # Add regions of this area to the list
        return_regions.extend((k.name, 1) for k in local_regions)

    return [return_areas, return_regions]


def get_embarkation_regions():
    areas = SearchQuerySet().models(ExportRegion)

    return_areas = [(k.name, 1) for k in areas]

    return [return_areas, ]


table_rows = [("Flag", "nation", get_flags()),
              ("Embarkation regions", "embarkation_region", get_embarkation_regions()),
              ("Broad disembarkation regions", "broad_disembarkation_region", get_broad_regions(ImportArea)),
              ("Specific disembarkation regions", "disembarkation_region", get_regions(ImportRegion, ImportArea, "import")),
              ("Individual years", ),
              ("5-year periods", ),
              ("10-year periods", ),
              ("25-year periods", ),
              ("50-year periods", ),
              ("100-year periods", )]

table_columns = [("Flag", "nation", get_flags()),
                 ("Embarkation regions", "embarkation_region", get_embarkation_regions()),
                 ("Broad disembarkation regions", "broad_disembarkation_region", get_broad_regions(ImportArea)),
                 ("Specific disembarkation regions", "disembarkation_region",
                  get_regions(ImportRegion, ImportArea, "import"))]

table_cells = [("Embarked/Disembarked", ),
               ("Only embarked", ),
               ("Only disembarked", )]




# These two have to be replaced with context processor call
# on database/solr
first_year = 1501
last_year = 1866