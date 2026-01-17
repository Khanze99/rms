import os

import requests

from airflow.models import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


class TelegramOperator(BaseOperator):
    def __init__(self, token, chat_id, **kwargs):
        super().__init__(**kwargs)
        self.url = f'https://api.telegram.org/bot{token}/sendMessage'
        self.chat_id = chat_id

    def execute(self, context):
        hook = PostgresHook(postgres_conn_id='postgres_default')
        schedule_events = hook.get_records(
            'SELECT id, name, link '
            'from rmsl_event '
            'where scheduled_at is not null and scheduled_at < now() and is_posted is False '
            'order by scheduled_at desc limit 1;'
        )
        if schedule_events:
            event = schedule_events[0]
            text = f"{event[1]}\n\n{event[2]}"
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            print(self.url, payload)
            print(os.getenv('TELEGRAM_BOT_TOKEN'))
            print(os.getenv('TELEGRAM_CHAT_ID'))
            response = requests.post(self.url, data=payload)
            if not response.ok:
                self.log.error('Failed to send message')
                response.raise_for_status()

            hook.run(
                'UPDATE rmsl_event SET is_posted = True where id = %s',
                parameters=(event[0], )
            )
