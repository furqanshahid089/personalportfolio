#!/bin/bash
# Vercel build step: install dependencies, run migrations, collect static files.
# This runs during the Vercel build. Static files are output to "staticfiles/".

set -e

python3 -m pip install -r requirements.txt

# Apply database migrations (safe to run every deploy; no-op if up to date).
# Only runs when a DATABASE_URL is configured, so a DB-less deploy won't fail.
if [ -n "$DATABASE_URL" ]; then
  python3 manage.py migrate --noinput
fi

# Gather static assets for WhiteNoise to serve.
python3 manage.py collectstatic --noinput --clear
