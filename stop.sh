#! /usr/bin/env bash
#
# stops all containers but postgres
#
./docker.sh stop airflow airflow-broker airflow-worker
