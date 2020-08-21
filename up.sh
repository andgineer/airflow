#! /usr/bin/env bash
# Start service(s) with build if necessary.
# Pass all params.
#
# Show logs.
# Example
#  ./up.sh airflow-db

./compose.sh \
  up -d --build \
  "$@"

./compose.sh logs -f "$@"
