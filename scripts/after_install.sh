#!/bin/bash
set -e

# Set useful variables
export APP_PATH=/home/datamade/scrapers-us-municipal
export VIRTUALENV=/home/datamade/.virtualenvs/opencivicdata

# Create virtual environment
# TODO: Determine why this fails on the OCD server
# python3 -m venv $VIRTUALENV

# Make sure everything you'd expect is owned by the datamade user
chown -R datamade.www-data /home/datamade
chown -R datamade.www-data $VIRTUALENV

# Install things into the correct virtual environment
$VIRTUALENV/bin/pip install --upgrade pip
$VIRTUALENV/bin/pip install -r $APP_PATH/requirements.txt --upgrade

# Move crontasks to correct place, and assign correct ownership and permissions.
mv $APP_PATH/scripts/scrapers-us-municipal-crontask /etc/cron.d/scrapers-us-municipal-crontask
chown root.root /etc/cron.d/scrapers-us-municipal-crontask
chmod 644 /etc/cron.d/scrapers-us-municipal-crontask

mv /home/datamade/scrapers-us-municipal/scripts/la-metro-crontask /etc/cron.d/la-metro-crontask
chown root.root /etc/cron.d/la-metro-crontask
chmod 644 /etc/cron.d/la-metro-crontask

# Run Migrations
cd $APP_PATH && DJANGO_SETTINGS_MODULE=pupa.settings $VIRTUALENV/bin/django-admin migrate
