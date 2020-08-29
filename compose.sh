#! /usr/bin/env bash
# run docker-compose with an arguments
#
# Example:
#   compose.sh logs airflow
#

. ./export_vars.sh

docker-compose \
  "$@"
