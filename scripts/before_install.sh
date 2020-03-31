#!/bin/bash

# Make directory for project. This may already exist but it's a good practice
# to make sure this pipeline will work on a bare server.
mkdir -p /home/datamade/scrapers-us-municipal

# Create and update permissions on logfile
touch /tmp/lametro.log
chown datamade.www-data /tmp/lametro.log

# Create directory for scraped data
mkdir -p /cache
chown -R datamade.www-data /cache

# Decrypt files encrypted with blackbox
cd /opt/codedeploy-agent/deployment-root/$DEPLOYMENT_GROUP_ID/$DEPLOYMENT_ID/deployment-archive/ && chown -R datamade.datamade . && sudo -H -u datamade blackbox_postdeploy