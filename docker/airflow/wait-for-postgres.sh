#!/bin/bash

set -e

host="$1"
port="$2"

timeout=60
counter=0
step=1

echo "Waiting for ${host}:${port}..."

until (</dev/tcp/${host}/${port}) 2>/dev/null; do
  counter=$((counter + step))
  if [ ${counter} -ge ${timeout} ]; then
    echo "Timeout reached. ${host}:${port} is not available."
    exit 1
  fi
  echo "Waiting for ${host}:${port}... ${counter}s"
  sleep ${step}
done

echo "Postgres is up and running"