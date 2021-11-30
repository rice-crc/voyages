###
### Ubuntu 1804 with default Python 3.6
###

# -- Base --

FROM ubuntu:18.04 AS base

RUN apt-get update -y \
  && apt-get install --yes --no-upgrade --no-install-recommends \
    gettext=0.19.8.1-6ubuntu0.3 \
    mysql-client=5.7.36-0ubuntu0.18.04.1 \
    libmysqlclient-dev=5.7.36-0ubuntu0.18.04.1 \
    python3=3.6.7-1~18.04 \
    python3-pip=9.0.1-2.3~ubuntu1.18.04.5 \
    python3-future=0.15.2-4ubuntu2 \
    python3-pygit2=0.26.2-2 \
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
    libxml2-dev=2.9.4+dfsg1-6.1ubuntu1.4 \
    libxslt1-dev=1.1.29-5ubuntu0.2 \
    python3-dev=3.6.7-1~18.04 \
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

EXPOSE $GUNICORN_PORT

CMD gunicorn --bind 0.0.0.0:$GUNICORN_PORT $GUNICORN_OPTS voyages.wsgi
