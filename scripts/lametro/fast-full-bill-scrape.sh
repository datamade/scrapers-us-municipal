#/bin/sh

(cd $APPDIR && \
    $PUPADIR update --datadir=/cache/bills/_data/ lametro --scrape bills --window=0 --rpm=0 && \
    $PUPADIR update --datadir=/cache/bills/_data/ lametro --import && \
    SHARED_DB=True DATABASE_URL=postgis://datamade@lametro-upgrade.datamade.us/lametro_staging pupa --datadir=/cache/bills/_data/ update lametro --import)
