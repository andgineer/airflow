#! /usr/bin/env bash
# run docker-compose with an arguments
#
# Example:
#   compose.sh logs airflow
#

. ./source_env.sh

docker-compose \
  "$@"
