#! /usr/bin/env bash
# exec docker-compose service with all arguments
# Pass all args to docker-compose
#
# Example:
#   exec.sh airflow

./docker.sh \
  exec \
  "$@" \
  bash

