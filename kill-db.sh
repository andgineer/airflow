#! /usr/bin/env bash
#
# DELETES Airflow DB !!!
#
./docker.sh stop
./docker.sh rm -f airflow airflow-db airflow-worker
docker volume rm airflow_postgres-airflow
./up.sh
./docker.sh logs -f airflow
