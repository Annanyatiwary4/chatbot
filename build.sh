#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

# ✅ Download NLTK resources
python -m nltk.downloader punkt
python manage.py collectstatic --no-input
python manage.py migrate
