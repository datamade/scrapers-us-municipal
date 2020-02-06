#!/bin/sh
set -e

exec 2>&1

cd $APPDIR
$PUPADIR update --datadir=/cache/bills/_data/ lametro --scrape bills --window=0 --rpm=0
# TODO: Uncomment this before production deployment.
# $PUPADIR update --datadir=/cache/bills/_data/ lametro --import
# TODO: Update database URL before production deployment on remote server.
SHARED_DB=True DATABASE_URL=postgis://datamade@localhost/lametro_staging $PUPADIR --datadir=/cache/bills/_data/ update lametro --import
