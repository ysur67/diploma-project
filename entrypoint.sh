#! /bin/bash

python ./project/manage.py makemigrations --no-input

python ./project/manage.py migrate --no-input

python ./project/manage.py collectstatic --no-input

exec gunicorn --chdir ./project project.wsgi:application -b 0.0.0.0:8000 --reload
