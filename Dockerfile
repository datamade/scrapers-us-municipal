FROM python:3.6-slim-stretch
LABEL maintainer "DataMade <info@datamade.us>"

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y libxml2-dev libxslt1-dev gdal-bin

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["/app/docker-entrypoint.sh"]