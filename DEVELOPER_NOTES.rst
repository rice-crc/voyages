Image Cache
===========

When using the `PIL <https://pypi.python.org/pypi/PIL/>`_ python library, thumbnail images are cached in ``/documents/cache``
Sometimes (especally after a code deploy) these files get out of sync and the thumbnail
images do not display. To correct this run the command::

  $ python manage.py thumbnail cleanup