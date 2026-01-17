import datetime
import os
import sys
import time

import feedparser
import pydantic
import psycopg2

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from plugins.operators.telegram import TelegramOperator


class Event(pydantic.BaseModel):
    name: str
    description: str
    link: str
    published_at: datetime.datetime
    scheduled_at: datetime.datetime | None
    resource_id: int


def _create_events(**context):
    # todo на каждый ресурс своя таска мб
    # todo add type of source rss, html or something other
    hook = PostgresHook(postgres_conn_id='postgres_default')

    records = hook.get_records('SELECT id, link from rmsl_resource;')
    last_event = hook.get_records(
        'SELECT scheduled_at from rmsl_event where scheduled_at is not null order by scheduled_at desc limit 1;'
    )

    last_event_published_at = last_event[0][0] if last_event else None

    events = []

    for record in records:
        _id, link_rss = record
        feed = feedparser.parse(link_rss)

        scheduled_at = last_event_published_at
        for entry in feed.entries:
            if scheduled_at:
                scheduled_at = scheduled_at + datetime.timedelta(hours=1)
            else:
                scheduled_at = datetime.datetime.now()
            title = entry.title
            external_source = entry.link
            published = datetime.datetime.fromtimestamp(
                time.mktime(entry.published_parsed)
            ).replace(tzinfo=datetime.timezone.utc)
            events.append(
                Event(
                    name=title,
                    description=title,
                    link=external_source,
                    published_at=published,
                    resource_id=_id,
                    scheduled_at=scheduled_at,
                )
            )

    rows = []
    for event in events:
        rows.append(
            (
                event.name,
                event.description,
                event.link,
                event.published_at,
                datetime.datetime.now(),  # todo mb we can add in init event model?
                event.resource_id,
                event.scheduled_at,
            )
        )

    try:
        hook.insert_rows(
            'rmsl_event',
            rows=rows,
            target_fields=['name', 'description', 'link', 'published_at', 'created_at', 'resource_id', 'scheduled_at']
        )
    except psycopg2.IntegrityError as e:  # todo need refactor that
        pass


with DAG(
    dag_id='resources',
    start_date=datetime.datetime.now() - datetime.timedelta(hours=1),
    schedule="@hourly",
    catchup=False,
) as dag:
    # tg send
    create_events = PythonOperator(
        task_id='create_events',
        python_callable=_create_events,
    )

    send_events = TelegramOperator(
        task_id='send_events',
        token=os.getenv('TELEGRAM_BOT_TOKEN'),
        chat_id=os.getenv('TELEGRAM_CHAT_ID'),
    )  # todo atomic and correct send post to tg
    create_events >> send_events
