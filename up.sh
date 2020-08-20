#! /usr/bin/env bash
# Start service(s) with build if necessary.
# Pass all params.
#
# Show logs.
# Example
#  ./up.sh airflow-db

./docker.sh \
  up -d --build \
  "$@"

./docker.sh logs -f "$@"
