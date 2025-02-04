#!/bin/bash

SERVER_PORT=${SERVER_PORT:-8000}

echo "Migrating database"
python manage.py migrate --noinput --run-syncdb

echo "Collecting Static Files"
python manage.py collectstatic --noinput

echo "Activating cron jobs"
python manage.py crontab add
service cron start
export > /opt/env

echo "Starting server"
gunicorn --bind 0.0.0.0:8000 server.wsgi:application --workers 3