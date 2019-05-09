Docker usage for development
============================

This project now contains a few files that help development using Docker.

Run 
  $ docker-compose build
to download mysql and solr images and also build
a new image that will run Django development server on the live source code.
This build process ensures that all python dependencies are installed.

Before the first usage, the database needs to be created.
  $ docker-compose run -p 3306:3306 voyages-mysql-service
Now you can connect to localhost:3306 and execute CREATE DATABASE voyages.
If you have a SQL file backed up from a running version of voyages, you can
use it at this point, otherwise follow DEPLOYNOTES to setup a fresh copy.

With the DB in order, you can launch all services together
  $ docker-compose up
The Solr index will be empty, however, so you can execute a rebuild_index
command inside the django service container. For that, run
  $ docker ps
and check the id of the django service, then run
  $ docker exec -it {django_service_container_id} /bin/bash
this should open a bash terminal inside the container, where you can execute
  # python /src/voyages/manage.py rebuild_index
This will take a while to finish.

When you are done working you can close the containers using
  $ docker-compose down

NOTE: a data/ folder will be created in the project's folder. Both the SQL DB
and Solr's index will be stored in that folder. The .gitignore file ensures that
those files are excluded from the version control.