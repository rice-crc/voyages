.. _DEPLOYNOTES:

Installation
============

Software dependencies
---------------------

We recommend the use of `pip <http://pip.openplans.org/>`_ and `virtualenv
<http://virtualenv.openplans.org/>`_ for environment and dependency management
in this and other Python projects. If you don't have them installed we
recommend ``sudo easy_install pip`` and then ``sudo pip install virtualenv``.

Configure the environment
~~~~~~~~~~~~~~~~~~~~~~~~~

When first installing this project, you'll need to create a virtual environment
for it. The environment is just a directory. You can store it anywhere you
like; in this documentation it'll live right next to the source. For instance,
if the source is in ``/home/httpd/voyages/src``, consider creating an
environment in ``/home/httpd/voyages/env``. To create such an environment, su
into apache's user and::

  $ virtualenv --no-site-packages /home/httpd/voyages/env

This creates a new virtual environment in that directory. Source the activation
file to invoke the virtual environment (requires that you use the bash shell)::

  $ . /home/httpd/voyages/env/bin/activate

Once the environment has been activated inside a shell, Python programs
spawned from that shell will read their environment only from this
directory, not from the system-wide site packages. Installations will
correspondingly be installed into this environment.

.. Note::
  Installation instructions and upgrade notes below assume that
  you are already in an activated shell.


Install python dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Voyages depends on several python libraries. The installation is mostly
automated, and will print status messages as packages are installed. If there
are any errors, pip should announce them very loudly.

To install python dependencies, cd into the repository checkout and::

  $ pip install -r requirments.txt

If you are a developer or are installing to a continuous ingration server
where you plan to run unit tests, code coverage reports, or build sphinx
documentation, you probably will also want to::

  $ pip install -r requirments/dev.txt

After this step, your virtual environment should contain all of the
needed dependencies.

Solr
~~~~~~~~~~~~~~~

Voyages uses `Solr <http://lucene.apache.org/solr/>`_
for searching and indexing Fedora content. The Solr schema
included with the source code at ``solr/schema.xml`` should be used as the
Solr schema configuration. For convenience, this directory also contains a
sample ``solrconfig.xml`` and minimal versions of all other solr
configuration files used by the index.

The url for accessing the configured Solr instance should be set in
``localsettings.py`` as **SOLR_SERVER_URL**.



Install the application
-----------------------

Apache
~~~~~~

After installing dependencies, copy and edit the wsgi and apache
configuration files in src/apache inside the source code checkout. Both may
require some tweaking for paths and other system details.

Configuration
~~~~~~~~~~~~~

Configure application settings by copying ``localsettings.py.dist`` to
``localsettings.py`` and editing for local settings (database, etc.).

After configuring all settings, initialize the db with all needed
tables and initial data using::

  $ python manage.py syncdb
  $ python manage.py migrate


Cron jobs
~~~~~~~~~

Session cleanup
^^^^^^^^^^^^^^^

The application uses database-backed sessions. Django recommends
periodically `clearing the session table <https://docs.djangoproject.com/en/1.3/topics/http/sessions/#clearing-the-session-table>`_
in this configuration. To do this, set up a cron job to run the following
command periodically from within the application's virtual environment::

  $ manage.py cleanup

This script removes any expired sessions from the database. We recommend
doing this about every week, though exact timing depends on usage patterns
and administrative discretion.