#! /usr/bin/env bash
# Start service(s) with build if necessary.
# Pass all params.
#
# Show logs.
# Example
#  ./up.sh airflow-db

mkdir -p etl/logs

./compose.sh \
  up -d --build \
  "$@"

./compose.sh logs --tail 50 -f "$@"
