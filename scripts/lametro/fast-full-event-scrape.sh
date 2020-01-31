#/bin/sh

(cd $APPDIR && \
    $PUPADIR update --datadir=/cache/events/_data/ lametro --scrape events --rpm=0 && \
    $PUPADIR update --datadir=/cache/events/_data/ lametro --import && \
    SHARED_DB=True DATABASE_URL=postgis://datamade@lametro-upgrade.datamade.us/lametro_staging pupa update --datadir=/cache/events/_data/ lametro --import)
