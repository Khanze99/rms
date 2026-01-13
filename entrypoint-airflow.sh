#!/bin/bash
set -e

# 1. Читаем секреты
PG_USER=$(cat /run/secrets/postgres_user)
PG_PASSWORD=$(cat /run/secrets/postgres_password)
POSTGRES_DB=$(cat /run/secrets/postgres_db)
DJ_SECRET_KEY=$(cat /run/secrets/django_secret_key)
DJ_DEBUG=$(cat /run/secrets/django_debug)
PG_NAME=$(cat /run/secrets/postgres_name)


export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://${PG_USER}:${PG_PASSWORD}@postgres:5432/${POSTGRES_DB}"
export AIRFLOW__CELERY__RESULT_BACKEND="db+postgresql://${PG_USER}:${PG_PASSWORD}@postgres:5432/${POSTGRES_DB}"

export DJANGO_SECRET_KEY=${DJ_SECRET_KEY}
export DJANGO_DEBUG=${DJ_DEBUG}
export POSTGRES_NAME=${PG_NAME}
export POSTGRES_USER=${POSTGRES_USER}
export POSTGRES_PASSWORD=${PG_PASSWORD}
export POSTGRES_HOST=$(cat /run/secrets/postgres_host)
export POSTGRES_PORT=$(cat /run/secrets/postgres_port)
export TELEGRAM_BOT_TOKEN=$(cat /run/secrets/tg_token)
export TELEGRAM_CHAT_ID=$(cat /run/secrets/chat_id)

exec /entrypoint "$@"
