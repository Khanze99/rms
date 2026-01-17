#!/bin/bash
set -e

export DJANGO_SECRET_KEY=$(cat /run/secrets/django_secret_key)
export DJANGO_DEBUG=$(cat /run/secrets/django_debug)
export POSTGRES_NAME=$(cat /run/secrets/postgres_user)
export POSTGRES_USER=$(cat /run/secrets/postgres_user)
export POSTGRES_PASSWORD=$(cat /run/secrets/postgres_password)
export POSTGRES_HOST=$(cat /run/secrets/postgres_host)
export POSTGRES_PORT=$(cat /run/secrets/postgres_port)

echo "=== Waiting for PostgreSQL ==="
until pg_isready -h postgres -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "=== Running migrations ==="
python manage.py migrate

echo "=== Collecting static files ==="
python manage.py collectstatic --no-input --clear --verbosity=2

echo "=== Verification ==="
echo "Static files in $(pwd)/static/:"
ls -la static/

echo "=== COMPLETE ==="
