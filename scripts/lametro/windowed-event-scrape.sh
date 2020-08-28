#!/bin/sh
set -e

exec 2>&1

cd $APPDIR
$PUPADIR update --datadir=/cache/events/_data/ lametro --scrape events window=$WINDOW
DATABASE_URL=postgis://datamade@3.93.9.229/lametro $PUPADIR update --datadir=/cache/events/_data/ lametro --import
$PUPADIR update --datadir=/cache/events/_data/ lametro --import
