#!/bin/bash

python manage.py makemigrations
python manage.py migrate
export DJANGO_SUPERUSER_PASSWORD=admin
# (re)create the default super admin user 
shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').delete()"
python manage.py createsuperuser --username admin --email admin@admin.com --noinput 

# Getting static files
python manage.py collectstatic --noinput

uwsgi --socket "0.0.0.0:${PORT}" --module entirety.wsgi --master --processes 4 --threads 2
