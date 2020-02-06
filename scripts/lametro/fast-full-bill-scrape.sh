#!/bin/sh
set -e

exec 2>&1

cd $APPDIR
$PUPADIR update --datadir=/cache/bills/_data/ lametro --scrape bills --window=0 --rpm=0
# TODO: Uncomment this before production deployment.
# $PUPADIR update --datadir=/cache/bills/_data/ lametro --import
SHARED_DB=True DATABASE_URL=postgis://datamade@lametro-upgrade.datamade.us/lametro_staging $PUPADIR --datadir=/cache/bills/_data/ update lametro --import
