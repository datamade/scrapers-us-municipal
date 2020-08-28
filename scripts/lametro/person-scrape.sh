#!/bin/sh
set -e

exec 2>&1

cd $APPDIR
$PUPADIR update --datadir=/cache/people/_data/ lametro --scrape people
DATABASE_URL=postgis://datamade@3.93.9.229/lametro $PUPADIR update --datadir=/cache/people/_data/ lametro --import people
$PUPADIR update --datadir=/cache/people/_data/ lametro --import people
