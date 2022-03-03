from voyages.apps.common.utils import BulkImportationHelper, SourceReferenceFinder
from voyages.apps.voyage.models import VoyageSources, VoyageSourcesType
from django.db import transaction

def import_sources(csv, log, live_admin_url="https://www.slavevoyages.org/admin/voyage/voyagesources/{}/change/"):
    """
    Imports a CSV file that includes plain-text source data, insert them on the
    database and produces Live Admin links that can be used to edit them.
    """
    helper = BulkImportationHelper()
    input_file = helper.read_to_dict(open(csv, 'rb'))
    sources = {}
    rows = [row for row in input_file]
    source_types = {t.group_name.lower(): t.id for t in VoyageSourcesType.objects.all()}
    has_errors = False
    for row in rows:
        short_ref = row['shortref']
        if len(short_ref) > 255:
            has_errors = True
            print("Source short_ref len should be <= 255: " + short_ref)
        full_ref = row['fullref']
        source_type = row['type'].lower()
        if source_type not in source_types:
            has_errors = True
            print("Source type not found: " + source_type)
        else:
            source_type = source_types[source_type]
        if short_ref in sources:
            # Check that the full_ref is identical.
            if full_ref != sources[short_ref].full_ref:
                has_errors = True
                print("Duplicate short_ref: " + short_ref)
        src = VoyageSources()
        src.short_ref = short_ref
        src.full_ref = full_ref
        src.source_type_id = source_type
        sources[short_ref] = src

    # Check whether the citations would match the new entry. We use the same
    # helper as the regular importation to not only reuse code but also ensure
    # consistency.
    ref_finder = SourceReferenceFinder(sources.values())
    for row in rows:
        citation = row['citation']
        (source, match) = ref_finder.get(citation)
        if source is None:
            has_errors = True
            print("Citation did not produce a match: " + citation)
        else:
            expected = sources[row['shortref']]
            if source != expected:
                has_errors = True
                print("Citation '{}' did not match expectation {}, instead {}".format(citation, expected.short_ref, source.short_ref))

    if not has_errors:
        with open(log, 'w') as f:
            f.write('<html><body>')
            with transaction.atomic():
                for src in sources.values():
                    src.save()
                    url = live_admin_url.format(src.pk)
                    output = "<a href=\"{}\">{}</a>".format(url, src.short_ref)
                    f.write(output) 
            f.write('</body></html>')

# Usage:
# from a shell, e.g. docker exec -i voyages-django bash -c 'python3 manage.py shell'
# from tools.automation.source_utils import *
# import_sources('path to csv', 'path to log')