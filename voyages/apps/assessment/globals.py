from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from haystack.query import SearchQuerySet

from .models import ExportRegion, ImportArea, ImportRegion, Nation


def nation_reset(search_configuration):
    if search_configuration is None:
        return False
    post_config = search_configuration["post"]
    if "submit nation" not in post_config:
        return False
    return post_config["submit_nation"] == "Reset to default"


def get_flags(search_configuration=None, _=None):
    if search_configuration is None:
        nations = [(k.name, 1) for k in SearchQuerySet().models(Nation)]
        return [
            nations,
        ]

    a = SearchQuerySet().models(Nation)
    nations = []

    for i in a:
        if "checkbox_nation_" + i.pk in search_configuration["post"] or \
                nation_reset(search_configuration):
            nations.append([i.name, 1])

    return [
        nations,
    ]


def get_broad_regions(search_configuration=None, _=None):
    areas_from_query = SearchQuerySet().models(ImportArea)

    if nation_reset(search_configuration):
        areas = [[k.name, 1] for k in areas_from_query]
    elif search_configuration is not None:
        areas = [[k.name, 1] if "darea-button-" + k.pk
                 in search_configuration["post"] else [k.name, 0]
                 for k in areas_from_query
                 if "darea-button-" + k.pk in search_configuration["post"]]
    else:
        areas = [[k.name, 1] for k in areas_from_query]

    return [
        areas,
    ]


def get_regions(search_configuration=None, _=None):
    return_areas = []
    return_regions = []
    areas = SearchQuerySet().models(ImportArea)

    # For each area, retrieve list of regions and add to the list with an
    # appropriate length
    for local_area in areas:

        # Retrieve regions
        local_regions = SearchQuerySet().models(ImportRegion).filter(
            import_area__exact=local_area.name)

        if (nation_reset(search_configuration) or
                (len(local_regions) == 1 and
                 "darea-button-" + local_area.pk
                 in search_configuration["post"])):
            local_regions_filtered = local_regions
        elif search_configuration is not None:
            local_regions_filtered = [
                k for k in local_regions
                if "dregion-button-" + k.pk in search_configuration["post"]
            ]
        else:
            local_regions_filtered = local_regions

        if len(local_regions_filtered) == 0:
            continue

        # Add the area
        return_areas.append([local_area.name, len(local_regions_filtered)])

        # Add regions of this area to the list
        return_regions.extend([k.name, 1] for k in local_regions_filtered)

    return [return_areas, return_regions]


def get_embarkation_regions(search_configuration=None, _=None):
    areas = SearchQuerySet().models(ExportRegion)

    if nation_reset(search_configuration):
        return_areas = [[k.name, 1] for k in areas]
    elif search_configuration is not None:
        return_areas = [[k.name, 1]
                        if "eregion-button-" + k.pk
                        in search_configuration["post"]
                        else [k.name, 0]
                        for k in areas
                        if "eregion-button-" + k.pk
                        in search_configuration["post"]]
    else:
        return_areas = [[k.name, 1] for k in areas]

    return [
        return_areas,
    ]


def get_incremented_year_tuples(search_configuration, mode):
    if mode == 4:
        interval = 1
    elif mode == 5:
        interval = 5
    elif mode == 6:
        interval = 10
    elif mode == 7:
        interval = 25
    elif mode == 8:
        interval = 50
    elif mode == 9:
        interval = 100

    first_year = search_configuration["year"]["year_from"]
    last_year = search_configuration["year"]["year_to"]

    if interval > 1:
        start_year = (int(first_year) - (int(first_year) % int(interval))) + 1
    else:
        start_year = (int(first_year) - (int(first_year) % int(interval)))
    current_year = start_year
    years = []
    while current_year <= last_year:
        if current_year + interval > last_year:
            right_year = last_year
        else:
            right_year = current_year + interval - 1
        years.append([current_year, right_year])
        current_year += interval

    return [
        years,
    ]


table_rows = [(_("Flag"), "nation__exact", get_flags),
              (_("Embarkation regions"),
               "embarkation_region__exact", get_embarkation_regions),
              (_("Broad disembarkation regions"),
               "broad_disembarkation_region__exact", get_broad_regions),
              (_("Specific disembarkation regions"),
               "disembarkation_region__exact", get_regions),
              (_("Individual years"), "year__in", get_incremented_year_tuples),
              (_("5-year periods"), "year__in", get_incremented_year_tuples),
              (_("10-year periods"), "year__in", get_incremented_year_tuples),
              (_("25-year periods"), "year__in", get_incremented_year_tuples),
              (_("50-year periods"), "year__in", get_incremented_year_tuples),
              (_("100-year periods"), "year__in", get_incremented_year_tuples)]

table_columns = [(_("Flag"), "nation__exact", get_flags),
                 (_("Embarkation regions"),
                  "embarkation_region__exact", get_embarkation_regions),
                 (_("Broad disembarkation regions"),
                  "broad_disembarkation_region__exact", get_broad_regions),
                 (_("Specific disembarkation regions"),
                  "disembarkation_region__exact", get_regions)]

table_cells = [(_("Embarked/Disembarked"),),
               (_("Only embarked"),),
               (_("Only disembarked"),)]

# These two have to be replaced with context processor call
# on database/solr
default_first_year = 1501
default_last_year = 1866


def get_map_year(frame_from_year, _):
    """
    Determine which base map should be loaded depending on the query's year
    range.
    :param frame_from_year: begin year.
    :param frame_to_year: end year.
    :return: one of four possible base map identifiers.
    """
    if frame_from_year >= 1808:
        return '1850'
    if frame_from_year >= 1642:
        return '1750'
    return '1650'
