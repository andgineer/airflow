#! /usr/bin/env bash
#
# Init DBs, Airflow Connections, start Airflow Scheduler, webUI & Flower
#

/entrypoint initdb
airflow connections --add --conn_id db_dev --conn_uri "${DEV_DB_URL}"
cd /
PYTHONPATH=/etl alembic upgrade head
(/entrypoint webserver &)
(/entrypoint flower &)
/entrypoint scheduler
