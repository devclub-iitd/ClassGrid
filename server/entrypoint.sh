#!/bin/bash

SERVER_PORT=${SERVER_PORT:-8000}

echo "Waiting for postgres..."
sleep 5
echo "Postgres started"

echo "Migrating database"
python manage.py migrate --noinput --run-syncdb

echo "Process 1"
python manage.py shell -c "from django.contrib.contenttypes.models import ContentType; ContentType.objects.all().delete()"

# echo "Process 2"
# python manage.py loaddata data-1.json

echo "Collecting Static Files"
python manage.py collectstatic --noinput

echo "Starting server"
gunicorn --bind 0.0.0.0:8000 server.wsgi:application --workers 3