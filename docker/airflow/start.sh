#! /usr/bin/env bash
#
# Init DBs, Airflow Connections, start Airflow Scheduler, webUI & Flower
#

./wait-for-postgres.sh "$AIRFLOW_DB_HOST" "$AIRFLOW_DB_PORT"

export AIRFLOW__CORE__AUTH_MANAGER=airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager

airflow db migrate
airflow connections add dev_db --conn-uri "${DEV_DB_URL}"
airflow connections add file_local --conn-extra "{\"path\": \"/ingest\"}" --conn-type fs
airflow users create --role Admin --username admin --email admin@example.com --firstname admin --lastname admin --password admin
cd /
PYTHONPATH=/etl alembic upgrade head

# Check for DAG parsing errors before starting services
echo "=== Checking DAG parsing ==="
export PYTHONPATH=/etl

# Force DAG serialization (this will clear and rebuild the serialized DAG table)
echo "=== Forcing DAG serialization ==="
airflow dags reserialize || echo "DAG reserialize failed"

airflow dags list --verbose || echo "DAG parsing failed - check logs above"

airflow api-server &
airflow celery flower &
airflow scheduler
