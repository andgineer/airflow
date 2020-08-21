#! /usr/bin/env bash
#
# DELETES Airflow DB !!!
#
./compose.sh stop
./compose.sh rm -f airflow airflow-db airflow-worker
docker volume rm airflow_postgres-airflow
./up.sh
./compose.sh logs -f airflow
