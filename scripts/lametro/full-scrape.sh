#!/bin/sh
set -e

exec 2>&1

cd $APPDIR

# Bills are windowed to 3 days by default. Scrape all people, all events, and
# windowed bills.
$PUPADIR update lametro --scrape
SHARED_DB=True DATABASE_URL=postgis://datamade@3.93.9.229/lametro $PUPADIR update lametro --import
SHARED_DB=True DATABASE_URL=postgis://datamade@3.93.9.229/lametro_staging $PUPADIR update lametro --import
$PUPADIR update lametro --import

# Scrape all bills.
$PUPADIR update lametro --scrape bills window=0
SHARED_DB=True DATABASE_URL=postgis://datamade@3.93.9.229/lametro $PUPADIR update lametro --import
SHARED_DB=True DATABASE_URL=postgis://datamade@3.93.9.229/lametro_staging $PUPADIR update lametro --import
$PUPADIR update lametro --import
