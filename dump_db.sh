#! /usr/bin/env bash
#
# Backup Airflow DB and ETL DB
#
POSTGRES_SERVICE_NAME="airflow-db"
. ./export_vars.sh # this line should be before we use $ETL_DB_*

DATE=`date +%y%m%d`

source container_is_not_running.sh

if container_is_not_running ${POSTGRES_SERVICE_NAME} ; then
    echo
    echo "Postgres container is not running!"
    echo
    echo "Use './up.sh ${POSTGRES_SERVICE_NAME}' to run the container."
    exit
fi

POSTGRES_USER=${AIRFLOW_DB_USER}
POSTGRES_DB=${AIRFLOW_DB_DB}
./compose.sh \
  exec \
  ${POSTGRES_SERVICE_NAME} pg_dump -U $POSTGRES_USER $POSTGRES_DB \
  > airflow_${DATE}.dump

tar -zcvf airflow_dump_${DATE}.tar.gz airflow_${DATE}.dump

POSTGRES_USER=${ETL_DB_USER}
POSTGRES_DB=${ETL_DB_DB}
./compose.sh \
  exec \
  ${POSTGRES_SERVICE_NAME} pg_dump -U $POSTGRES_USER $POSTGRES_DB \
  > etl_${DATE}.dump

tar -zcvf etl_dump_${DATE}.tar.gz etl_${DATE}.dump
