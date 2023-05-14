#! /usr/bin/env bash
#
# Init DBs, Airflow Connections, start Airflow Scheduler, webUI & Flower
#

airflow db init
airflow connections --add --conn_id dev_db --conn_uri "${DEV_DB_URL}"
airflow connections --add --conn_id file_local --conn_extra "{\"path\": \"/ingest\"}" --conn_type fs
cd /
PYTHONPATH=/etl alembic upgrade head
airflow webserver &
airflow celery flower &
airflow scheduler
