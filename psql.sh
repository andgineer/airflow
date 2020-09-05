#! /usr/bin/env bash
#
# run psql for ETL/Airflow DB in postgres container
# default is ETL DB.
# To connect to airflow DB use
#   ./psql.sh airflow
#
POSTGRES_SERVICE_NAME="airflow-db"
. ./export_vars.sh # this line should be before we use $ETL_DB_*

case $1 in
     airflow)
          POSTGRES_USER=${AIRFLOW_DB_USER}
          POSTGRES_DB=${AIRFLOW_DB_DB}
          ;;
     *)
          POSTGRES_USER=${ETL_DB_USER}
          POSTGRES_DB=${ETL_DB_DB}
          ;;
esac

echo "Service: ${POSTGRES_SERVICE_NAME}, user: $POSTGRES_USER, db: $POSTGRES_DB"

source container_is_not_running.sh

if container_is_not_running ${POSTGRES_SERVICE_NAME} ; then
    echo
    echo "Postgres container is not running!"
    echo
    echo "Use './up.sh ${POSTGRES_SERVICE_NAME}' to run the container."
    exit
fi

./exec.sh ${POSTGRES_SERVICE_NAME} psql -U $POSTGRES_USER -d $POSTGRES_DB
