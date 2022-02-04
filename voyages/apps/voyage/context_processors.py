from __future__ import unicode_literals

from voyages.apps.voyage.globals import calculate_maxmin_years


def voyage_span(_):
    """
    Obtain the first and last year when voyages began
    """
    first, last = calculate_maxmin_years()
    return {
        'voyage_span_first_year': first,
        'voyage_span_last_year': last,
    }
