#!/bin/bash
set -e

# 1. Читаем секреты
POSTGRES_DB=$(cat /run/secrets/postgres_db)

export DJANGO_SECRET_KEY=$(cat /run/secrets/django_secret_key)
export DJANGO_DEBUG=$(cat /run/secrets/django_debug)
export POSTGRES_NAME=$(cat /run/secrets/postgres_user)
export POSTGRES_USER=$(cat /run/secrets/postgres_user)
export POSTGRES_PASSWORD=$(cat /run/secrets/postgres_password)
export POSTGRES_HOST=$(cat /run/secrets/postgres_host)
export POSTGRES_PORT=$(cat /run/secrets/postgres_port)

echo "Testing PostgreSQL connection..."
until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1" >/dev/null 2>&1; do
  echo "PostgreSQL not ready, waiting..."
  sleep 5
done

echo "PostgreSQL is ready!"

cd /opt/airflow/admin
exec uvicorn --host 0.0.0.0 --port 8000 --workers 2 --log-level info rmsa.asgi:application
