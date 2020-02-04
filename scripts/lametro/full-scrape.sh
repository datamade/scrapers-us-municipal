#/bin/sh
set -e

exec 2>&1

cd $APPDIR

# Bills are windowed to 3 days by default. Scrape all people, all events, and
# windowed bills.
$PUPADIR update lametro --scrape
$PUPADIR update lametro --import
SHARED_DB=True DATABASE_URL=postgis://datamade@lametro-upgrade.datamade.us/lametro_staging pupa update lametro --import

# Scrape all bills.
$PUPADIR update lametro --scrape bills window=0
$PUPADIR update lametro --import
SHARED_DB=True DATABASE_URL=postgis://datamade@lametro-upgrade.datamade.us/lametro_staging pupa update lametro --import
