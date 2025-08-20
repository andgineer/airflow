#! /usr/bin/env bash
#
# Start Airflow (Celery) Worker
#

# Configure FAB auth manager
export AIRFLOW__CORE__AUTH_MANAGER=airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager

# Set execution API server URL for worker to connect to execution API endpoint
export AIRFLOW__CORE__EXECUTION_API_SERVER_URL=http://airflow:8080/execution/

# Airflow API authentication (see airflow.cfg#api.secret_key)
export AIRFLOW__API_AUTH__JWT_SECRET=314985712395t9342yt9y24go9fyog94rh_jwt_api_auth

# wait for Airflow DB to be initialized in airflow container
sleep 10

airflow celery worker
