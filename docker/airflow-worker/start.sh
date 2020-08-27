#! /usr/bin/env bash
#
# Start Airflow (Celery) Worker
#

# wait for Airflow DB to be be initialized in airflow container
sleep 10

airflow worker
