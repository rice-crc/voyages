# Development

[Home](../README.md)

## Table of Contents

* [Getting Started](#getting-started)
  * [System Requirements](#system-requirements)
  * [Fork and Clone the Project](#fork-and-clone-the-project)
  * [Installation](#installation)
* [TLDR Workflow](#tldr-workflow)
* [Development Workflow](#development-workflow)
  * [Update Your Fork](#update-your-fork)
  * [Do Your Work](#do-your-work)
  * [Make a Pull Request](#make-a-pull-request)
  * [Clean Up Your Work](#clean-up-your-work)
* [Deployment Workflow](#deployment-workflow)
* [Frequently Asked Questions](#frequently-asked-questions)
* [Miscellanious Tasks](#miscellanious-tasks)

## Getting Started

To set up your local environment and begin developing for this project, complete the following steps.

### System Requirements

*Note: This document is geared toward MacOS but can be easily applied to Linux. Contribution for Windows users is welcome.*

For reference, this document was written while testing on a 2018 MacBook Pro running MacOS Big Sur and Docker Desktop 3.2.2.

Make sure the Xcode Command Line Tools are installed.

```bash
host:~$ sudo xcodebuild -license
host:~$ xcode-select --install
```

Install Homebrew.

```bash
host:~$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Install Docker Desktop.

```bash
host:~$ brew install --cask docker
```

Due to resource utilization in the application, it is recommended to increase memory available to containers.

In Docker Desktop, visit Settings > Resources > Advanced. Set "Memory" to at least 4GB.

[Return to Top](#table-of-contents)

### Fork and Clone the Project

Visit GitHub and navigate to the [rice-crc/voyages](https://github.com/rice-crc/voyages) repository.  In the top-right corner of the page, click the "Fork" button.

For more information, check GitHub's documentation on [forking repositories](https://help.github.com/articles/fork-a-repo/).

Clone the fork to your local machine.

```bash
host:~/Projects$ git clone https://github.com/<username>/voyages.git
```

Add the parent repository as an upstream remote.

```bash
host:~/Projects$ cd voyages

host:~/Projects/voyages$ git remote add upstream https://github.com/rice-crc/voyages.git
```

[Return to Top](#table-of-contents)

## Installation

Copy and rename the default localsettings file for local environments.

```bash
host:~/Projects/voyages$ cp voyages/localsettings-local.py.default voyages/localsettings.py
```

Build and run the containers necessary to work on the project.

For details, see `docker-compose.yml`.

```bash
host:~/Projects/voyages$ docker-compose up -d --build
```

Create the database.

```bash
host:~/Projects/voyages$ docker exec -i voyages-mysql mysql -uroot -pvoyages -e "create database voyages"
```

Create the database user and grant privileges.

```bash
host:~/Projects/voyages$ docker exec -i voyages-mysql mysql -uroot -pvoyages -e "create user 'voyages'@'%' identified by 'voyages'"
host:~/Projects/voyages$ docker exec -i voyages-mysql mysql -uroot -pvoyages -e "grant all on voyages.* to 'voyages'@'%'"
```

Download the latest `emory-voyages_prod-*.sql.tgz` MySQL dump from the Google Drive share and expand to the `data/voyages_prod.sql` file.

Import the database dump to MySQL.

```bash
host:~/Projects/voyages$ docker exec -i voyages-mysql mysql -uroot -pvoyages voyages < data/voyages_prod.sql
```

Verify the data import.

```mysql
host:~/Projects/voyages$ docker exec -i voyages-mysql mysql -uvoyages -pvoyages -e "show databases"
host:~/Projects/voyages$ docker exec -i voyages-mysql mysql -uvoyages -pvoyages -e "show tables from voyages"
host:~/Projects/voyages$ docker exec -i voyages-mysql mysql -uvoyages -pvoyages -e "select * from voyages.voyage_voyage limit 1"
```

Create the Solr index.

```bash
host:~/Projects/voyages$ docker exec -i voyages-solr solr create_core -c voyages -d /srv/voyages/solr
```

Run the process to build the index. This will take a very long time (around 60-90 minutes).

```bash
host:~/Projects/voyages$ docker exec -i voyages-django bash -c 'python3 manage.py rebuild_index --noinput'
```

Run media asset tasks. These may also take a very long time.

```bash
host:~/Projects/voyages$ docker exec -i voyages-django bash -c 'python3 manage.py compilemessages'
host:~/Projects/voyages$ docker exec -i voyages-django bash -c 'python3 manage.py compilescss'
host:~/Projects/voyages$ docker exec -i voyages-django bash -c 'python3 manage.py collectstatic --noinput'
host:~/Projects/voyages$ docker exec -i voyages-django bash -c 'python3 manage.py compress --force'
host:~/Projects/voyages$ docker exec -i voyages-django bash -c 'python3 manage.py thumbnail cleanup'
```

Note the following project resources:

* Voyages app: [http://127.0.0.1:8100/](http://127.0.0.1:8100/).
* Solr: [http://127.0.0.1:8983](http://127.0.0.1:8983)
* Adminer: [http://127.0.0.1:8080](http://127.0.0.1:8080)
* Mailhog: [http://127.0.0.1:8025](http://127.0.0.1:8025)

[Return to Top](#table-of-contents)

## TLDR Workflow

The following is meant to be a concise reference for the development process.

For more details, check the full [Development Workflow](#development-workflow) section below.

```bash
# Setup.

git clone https://github.com/<username>/voyages.git
cd voyages

# Any time you start new work, make sure your develop branch is up-to-date
# with the remote on GitHub.

git checkout develop
git fetch upstream && git rebase upstream/develop

# Create a working branch to isolate your changes and begin your work.

git checkout -b short-desc

# Before any commit, always make sure your branch is up-to-date with the remote.

# When your work is complete, pull the latest changes, resolve any merge
# conflicts, and then commit your work.

git fetch upstream && git rebase upstream/develop
git add . && git commit

# When ready, push your branch to your fork. Visit the repository on GitHub
# and make a Pull Request.

git push origin HEAD

# Once the Pull Request is accepted and merged, clean up your work.

git checkout develop && git branch -D short-desc
git fetch upstream && git rebase upstream/develop
git push
```

Visit the repository on GitHub to make a Pull Request.

[Return to Top](#table-of-contents)

## Development Workflow

There are two protected branches in the repository: main and develop (which serves as an integration branch).

### Update Your Fork

Ensure your fork is current and that you have the latest changes from the upstream develop branch.

```bash
host:~/Projects/voyages (develop)$ git fetch upstream
```

Rebase the upstream repository's develop branch.

```bash
host:~/Projects/voyages (develop)$ git rebase upstream/develop
```

Your local develop branch is now up-to-date with upstream.

To update your fork on GitHub, push your changes.

```bash
host:~/Projects/voyages (develop)$ git push
```

[Return to Top](#table-of-contents)

### Do Your Work

Continue your development work.

#### Create a Working Branch

Create a new local branch using the naming convention "short-desc".

```bash
host:~/Projects/voyages (develop)$  git checkout -b short-desc
```

#### Stage & Commit Your Work

Do the work required.

Stage your changes and commit as needed.  Each commit should be logically atomic.

```bash
host:~/Projects/voyages (short-desc *)$ git add .
host:~/Projects/voyages (short-desc +)$ git commit
```

#### Formatting Commit Messages

Use the following convention for commit messages.

* The first line should follow the pattern: "A short, grammatically correct sentence ending with punctuation."
* Enter a line break for the second line.
* Beginning with the third line, describe in detail what has changed and why.  Markdown lists can be used and will be displayed in GitHub.

#### Pull the Latest Upstream Changes

Ensure no additional changes have been made to the upstream repository and rebase if necessary.

```bash
host:~/Projects/voyages (short-desc)$ git fetch upstream
host:~/Projects/voyages (short-desc)$ git rebase upstream/develop
```

#### Push Your Working Branch

Push your local branch to your forked repository (origin) so that a Pull Request may be created.

```bash
host:~/Projects/voyages (short-desc)$ git push origin HEAD
```

[Return to Top](#table-of-contents)

### Make a Pull Request

On GitHub, navigate to your forked repository and create a new pull request against upstream/develop which describes the proposed changes.

[Return to Top](#table-of-contents)

### Clean Up Your Work

Once the pull request has been reviewed, approved, and merged into the upstream repository, clean up your work.

#### Delete the Working Branch

```bash
host:~/Projects/voyages (short-desc)$ git checkout develop
host:~/Projects/voyages (develop)$ git branch -D short-desc
```

#### Update Your Fork

```bash
host:~/Projects/voyages (develop)$ git fetch upstream
host:~/Projects/voyages (develop)$ git rebase upstream/develop

host:~/Projects/voyages (develop)$ git push
```

[Return to Top](#table-of-contents)

## Deployment Workflow

The OCI build instance pulls updates from the main branch in `rice-crc/voyages` every five minutes.

When changes are received, an offline Django container is automatically built on each of the remote app instances.

Once complete, Nginx containers on the app instances are updated to point at the new Django containers.

The new containers are live and the now-offline containers are removed.

[Return to Top](#table-of-contents)

## Frequently Asked Questions

### Is data persisted between restarts of the containers?

Yes, using Docker named volumes.

Be careful if you remove the MySQL and Solr volumes as you'll need to rerun the lengthy reindex.

### How can I blow away my local copy of the project and restart?

Remove the containers.

```bash
host:~/Projects/voyages$ docker-compose down
host:~/Projects/voyages$ docker container prune
host:~/Projects/voyages$ docker image prune
host:~/Projects/voyages$ docker network prune
host:~/Projects/voyages$ docker volume prune
```

Remove the local directory.

```bash
host:~/Projects/voyages$ cd ..
host:~/Projects$ rm -rf voyages
```

Begin from “Getting Started” > “Fork & Clone the Project”

[Return to Top](#table-of-contents)

## Miscellanious Tasks

```bash
# List running containers

docker ps

# View container logs

docker logs --tail 50 --follow --timestamps <id>

# View container resource statistics

docker ps -q | xargs docker stats --no-stream
docker ps -q | xargs docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" --no-stream

# View container size statistics

docker system df

# Connect to a container

docker exec -it <name> bash

# Rebuild a single container

docker-compose up -d --build <name>

# Run a command on a container

docker exec -i bash -c 'echo hello'
```

[Return to Top](#table-of-contents)
