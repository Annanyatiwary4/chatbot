#!/usr/bin/env bash
set -o errexit

pip install --no-cache-dir -r requirements.txt  # save memory
python -m nltk.downloader punkt
python manage.py collectstatic --no-input
python manage.py migrate

gunicorn chatbot.wsgi:application --bind 0.0.0.0:$PORT --workers=1
