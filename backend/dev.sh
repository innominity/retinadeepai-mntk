#!/bin/bash
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate --no-input
celery -A backend worker -l info --concurrency=2 --detach
celery -A backend worker -n worker1@%h -Q retina_detection --concurrency=2 -l info --detach 
#celery -A backend worker -n worker2@%h -Q retina_analysis --concurrency=1 -l info --detach
#celery --broker=redis://redis:6379/0 flower --port=5555 --detach
gunicorn backend.wsgi -b 0.0.0.0:8000 --timeout 600 --workers 5
