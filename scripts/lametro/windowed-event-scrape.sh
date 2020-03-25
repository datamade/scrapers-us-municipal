#!/bin/sh
set -e

exec 2>&1

cd $APPDIR
$PUPADIR update --datadir=/cache/events/_data/ lametro --scrape events window=$WINDOW
# TODO: Uncomment this before production deployment.
# $PUPADIR update --datadir=/cache/events/_data/ lametro --import
# TODO: Update database URL before production deployment on remote server.
SHARED_DB=True DATABASE_URL=postgis://datamade@localhost/lametro $PUPADIR update --datadir=/cache/events/_data/ lametro --import
SHARED_DB=True DATABASE_URL=postgis://datamade@localhost/lametro_staging $PUPADIR update --datadir=/cache/events/_data/ lametro --import
