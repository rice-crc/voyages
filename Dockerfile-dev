FROM ubuntu AS base
RUN apt-get update && apt-get install python python-pip python-dev libmysqlclient-dev git libxslt-dev gcc libxml2-dev mysql-client -y

FROM base AS voyages-dev
WORKDIR /src
COPY requirements.txt .
COPY requirements/ ./requirements/
RUN pip install -r requirements.txt
RUN pip install -r requirements/dev.txt
