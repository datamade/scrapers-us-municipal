#!/bin/sh
set -e

exec 2>&1

cd $APPDIR
$PUPADIR update --datadir=/cache/bills/_data/ lametro --scrape bills window=$WINDOW
SHARED_DB=True DATABASE_URL=postgis://datamade@3.93.9.229/lametro $PUPADIR update --datadir=/cache/bills/_data/ lametro --import
$PUPADIR update --datadir=/cache/bills/_data/ lametro --import
