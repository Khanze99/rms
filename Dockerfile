FROM apache/airflow:3.1.5

RUN pip install apache-airflow==3.1.5 \
    feedparser==6.0.12  \
    apache-airflow-providers-postgres==6.5.1 \
    django==6.0 \
    psycopg2-binary==2.9.11 \
    pydantic==2.12.5 \
    uvicorn==0.40.0

USER root

RUN chown -R airflow:root /opt/airflow && \
    chmod -R 775 /opt/airflow


COPY . /opt/airflow/
RUN chmod +x /opt/airflow/admin/django_entrypoint.sh
RUN chmod +x /opt/airflow/admin/migrate.sh
RUN chmod +x /opt/airflow/entrypoint-airflow.sh

USER airflow


ENTRYPOINT ["/bin/bash", "/opt/airflow/entrypoint-airflow.sh"]
