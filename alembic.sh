#! /usr/bin/env bash
# exec or run alembic in backend container
# Pass all args to it
#
# Example:
#   alembic.sh history

SERVICE_NAME="airflow"

source container_is_not_running.sh
args="$@"

if container_is_not_running ${SERVICE_NAME} ; then
  echo "Using RUN instead of EXEC"
  ./run.sh \
    ${SERVICE_NAME} \
    bash -c \
    "cd / && PYTHONPATH=etl alembic $args"
else
  ./compose.sh \
    exec \
    ${SERVICE_NAME} \
    bash -c \
    "cd / && PYTHONPATH=etl alembic $args"
fi