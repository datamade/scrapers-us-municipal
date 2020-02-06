#!/bin/sh
set -e

exec 2>&1

cd $APPDIR

# Bills are windowed to 3 days by default. Scrape all people, all events, and
# windowed bills.
$PUPADIR update lametro --scrape
# TODO: Uncomment this before production deployment.
# $PUPADIR update lametro --import
# TODO: Update database URL before production deployment on remote server.
SHARED_DB=True DATABASE_URL=postgis://datamade@localhost/lametro_staging $PUPADIR update lametro --import

# Scrape all bills.
$PUPADIR update lametro --scrape bills window=0
# TODO: Uncomment this before production deployment.
# $PUPADIR update lametro --import
# TODO: Update database URL before production deployment on remote server.
SHARED_DB=True DATABASE_URL=postgis://datamade@localhost/lametro_staging $PUPADIR update lametro --import
