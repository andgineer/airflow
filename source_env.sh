#! /usr/bin/env bash
# Export DB parameters for the environment.
# Do not forget to source it so the variables will be set in you session.
#
# Examples:
#   . ./source_env.sh
#

set -o allexport  # enables all following variable definitions to be exported
for env_file in env/airflow_db.env env/etl_db.env env/dev_db.env; do
  source $env_file
done
set +o allexport
