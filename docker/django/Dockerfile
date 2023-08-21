###
### Ubuntu 20.04 with default Python 3.6
###

# -- Base --

FROM ubuntu:20.04 AS base

RUN apt-get update -y \
  && apt-get install --yes --no-upgrade --no-install-recommends \
    gettext \
    mysql-client-8.0 \
    libmysqlclient-dev \
    python3 \
    python3-pip \
    python3-future \
    python3-pygit2 \
  && apt-get clean \
  && rm -rf \
    /tmp/* \
    /usr/share/doc/* \
    /var/cache/apt/* \
    /var/lib/apt/lists/* \
    /var/tmp/*

# -- Build --

FROM base AS build

RUN apt-get update \
  && apt-get install --yes --no-upgrade --no-install-recommends \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    python3-dev \
  && apt-get clean \
  && rm -rf \
    /tmp/* \
    /usr/share/doc/* \
    /var/cache/apt/* \
    /var/lib/apt/lists/* \
    /var/tmp/*

WORKDIR /srv/voyages

RUN python3 -m pip install --user --no-cache-dir --upgrade \
    pip==21.0.1  \
    setuptools==44.1.1 \
    wheel==0.36.2

COPY requirements/*.txt requirements/
RUN python3 -m pip install --user --no-cache-dir -r requirements/dev.txt

# -- Release --

FROM base AS release

WORKDIR /srv/voyages

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=/root/.local/bin:$PATH

COPY --from=build /root/.local /root/.local
COPY . .

ARG GUNICORN_PORT="8000"
ARG GUNICORN_OPTS="--reload --workers 3 --threads 2 --worker-class gthread"

ENV GUNICORN_PORT=${GUNICORN_PORT}
ENV GUNICORN_OPTS=${GUNICORN_OPTS}
# Calling Python's print() on an UTF-8 string might fail if this env var is not set.
ENV PYTHONIOENCODING=utf-8

EXPOSE $GUNICORN_PORT

CMD gunicorn --bind 0.0.0.0:$GUNICORN_PORT $GUNICORN_OPTS voyages.wsgi
