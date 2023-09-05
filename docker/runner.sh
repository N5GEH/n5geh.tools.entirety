#!/bin/bash

python manage.py makemigrations
python manage.py migrate

# Getting static files
python manage.py collectstatic --noinput

uwsgi --socket "0.0.0.0:${PORT}" --module entirety.wsgi --master --processes 4 --threads 2
