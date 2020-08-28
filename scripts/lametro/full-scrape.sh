#!/bin/sh
set -e

exec 2>&1

cd $APPDIR

# Bills are windowed to 3 days by default. Scrape all people, all events, and
# windowed bills.
$PUPADIR update lametro --scrape
DATABASE_URL=postgis://datamade@3.93.9.229/lametro $PUPADIR update lametro --import
$PUPADIR update lametro --import

# Scrape all bills.
$PUPADIR update lametro --scrape bills window=0
DATABASE_URL=postgis://datamade@3.93.9.229/lametro $PUPADIR update lametro --import
$PUPADIR update lametro --import
