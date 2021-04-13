Image Cache
===========

When using the `PIL <https://pypi.python.org/pypi/PIL/>`_ python library, thumbnail images are cached in ``/documents/cache``
Sometimes (especally after a code deploy) these files get out of sync and the thumbnail
images do not display. To correct this run the command::

  $ python manage.py thumbnail cleanup


Add Flat Page
=============
This example creates a new flat page in the education app.

1. create url.py entry in appropriate urls.py file:
url(r'new-page', django.contrib.flatpages.views.flatpage,
 {'url': '/education/new-page/'}, name='new-page')

2. In the Live Admin navigate to Flat pages and create a new entry with:
URL: /education/new-page/
Title: New Page
Content: HTML CONTENT
Template_Name: flatpages/education_flatpage.html
NOTE: The Template_Name field is under Advanced > Show on each flat page record.
      Since each app has its own styling requirements, each app should have its own base flat page.
      flatpages/education_flatpage.html  can be used as a starting point if additional templaes need to be added.

3. Make reference to the link { url ‘new-page’} somewhere on the website

4. export to initial data::

  $ python ./manage.py dumpdata flatpages --indent=4 > initialdata/flatpages.json

5. Load data to QA or Prod database
Make a copy of the initialdata/flatpages.json.
Remove the entries that are NOT new so any previous modifications are not overwritten::

  $ python ./manage.py loaddata <PATH-TO-INPUT-FILE>

