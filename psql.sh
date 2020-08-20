#! /usr/bin/env bash
#
# run psql in postgres container
#
POSTGRES_CREDENTIALS="env/etl_db.env"
POSTGRES_SERVICE_NAME="airflow-db"

export $(grep -v '^#' ${POSTGRES_CREDENTIALS} | xargs)

source container_is_not_running.sh

if container_is_not_running ${POSTGRES_SERVICE_NAME} ; then
    echo
    echo "Postgres container is not running!"
    echo
    echo "Use './up.sh ${POSTGRES_SERVICE_NAME}' to run the container."
    exit
fi

./exec.sh ${POSTGRES_SERVICE_NAME} psql -U $POSTGRES_USER -d $POSTGRES_DB "$@"
