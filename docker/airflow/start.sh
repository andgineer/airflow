#! /usr/bin/env bash
#
# Init DBs, Airflow Connections, start Airflow Scheduler, webUI & Flower
#

./wait-for-postgres.sh "$AIRFLOW_DB_HOST" "$AIRFLOW_DB_PORT"

airflow db migrate
airflow connections add dev_db --conn-uri "${DEV_DB_URL}"
airflow connections add file_local --conn-extra "{\"path\": \"/ingest\"}" --conn-type fs
airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
cd /
PYTHONPATH=/etl alembic upgrade head
airflow webserver &
airflow celery flower &
airflow scheduler
