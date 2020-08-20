#! /usr/bin/env bash
# run shell in docker-compose service without deps
# removes container after exit
#
# Examples:
# run.sh airflow

./docker-compose.sh \
  run --no-deps --rm \
  "$@"
