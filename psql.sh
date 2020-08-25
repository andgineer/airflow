#! /usr/bin/env bash
#
# run psql for ETL DB in postgres container
#
POSTGRES_SERVICE_NAME="airflow-db"
CREDENTIALS="env/etl_db.env"
. ./source_env.sh  # this line should be before we use env vars
POSTGRES_USER=${ETL_DB_USER}
POSTGRES_DB=${ETL_DB_DB}

echo "Service ${POSTGRES_SERVICE_NAME} user $POSTGRES_USER data $POSTGRES_DB"

source container_is_not_running.sh

if container_is_not_running ${POSTGRES_SERVICE_NAME} ; then
    echo
    echo "Postgres container is not running!"
    echo
    echo "Use './up.sh ${POSTGRES_SERVICE_NAME}' to run the container."
    exit
fi

./exec.sh ${POSTGRES_SERVICE_NAME} psql -U $POSTGRES_USER -d $POSTGRES_DB "$@"
