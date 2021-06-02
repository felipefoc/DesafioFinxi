#!/bin/sh

ls

echo "Running makemigrations"
python manage.py makemigrations

echo "Running migrate"
python manage.py migrate

echo "Loading Data"
python manage.py loaddata data.json

echo "Starting Server"
python manage.py runserver 0.0.0.0:8000

