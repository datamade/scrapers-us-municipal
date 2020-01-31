#/bin/sh

(cd $APPDIR && \
    $PUPADIR update lametro --scrape && \
    $PUPADIR update lametro --import && \
    SHARED_DB=True DATABASE_URL=postgis://datamade@lametro-upgrade.datamade.us/lametro_staging pupa update lametro --import && \
    $PUPADIR update lametro --scrape bills window=0 && \
    $PUPADIR update lametro --import && \
    SHARED_DB=True DATABASE_URL=postgis://datamade@lametro-upgrade.datamade.us/lametro_staging pupa update lametro --import)
