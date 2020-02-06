#!/bin/sh
set -e

exec 2>&1

cd $APPDIR
$PUPADIR update --datadir=/cache/events/_data/ lametro --scrape events window=$WINDOW
# TODO: Uncomment this before production deployment.
# $PUPADIR update --datadir=/cache/events/_data/ lametro --import
SHARED_DB=True DATABASE_URL=postgis://datamade@lametro-upgrade.datamade.us/lametro_staging pupa update --datadir=/cache/events/_data/ lametro --import
