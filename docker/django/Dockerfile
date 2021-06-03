# -- Base --

FROM ubuntu:18.04 AS base

RUN apt-get update \
  && apt-get install --yes --no-upgrade --no-install-recommends \
    gettext=0.19.8.1-6ubuntu0.3 \
    mysql-client=5.7.34-0ubuntu0.18.04.1 \
    libmysqlclient-dev=5.7.34-0ubuntu0.18.04.1 \
    python=2.7.15~rc1-1 \
    python-pip=9.0.1-2.3~ubuntu1.18.04.4 \
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
    gcc=4:7.4.0-1ubuntu2.3 \
    libxml2-dev=2.9.4+dfsg1-6.1ubuntu1.3 \
    libxslt1-dev=1.1.29-5ubuntu0.2 \
    python-dev=2.7.15~rc1-1 \
  && apt-get clean \
  && rm -rf \
    /tmp/* \
    /usr/share/doc/* \
    /var/cache/apt/* \
    /var/lib/apt/lists/* \
    /var/tmp/*

WORKDIR /srv/voyages

RUN python -m pip install --user --no-cache-dir --upgrade \
    pip==20.3.4  \
    setuptools==44.1.1 \
    wheel==0.36.2

COPY requirements/common.txt requirements/
RUN python -m pip install --user --no-warn-script-location --no-cache-dir -r requirements/common.txt
RUN mkdir logs

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

EXPOSE $GUNICORN_PORT

CMD gunicorn --bind 0.0.0.0:$GUNICORN_PORT $GUNICORN_OPTS voyages.wsgi
