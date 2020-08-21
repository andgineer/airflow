#! /usr/bin/env bash
#
# stops all containers but postgres
#
./compose.sh stop airflow airflow-broker airflow-worker
