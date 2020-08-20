# Apach Airflow

Template for local debugging Apache Airflow DAGs.
You can start local Airflow scheduler and workers with live reload of DAGs.

## How to run

    mkdir -p /etl/logs  # you have to create it manually so it will have right permissions
    docker-compose up --build
    
Airflow: http://127.0.0.1:8080/admin/
Flower: http://127.0.0.1:5551/dashboard

ETL tasks (DAGs) are in `etl/`.
We should copy this folder to all machines with airflow scheduler (service
`airflow` in the `docker-compose.yml`) and airflow wokers (service `worker`).

For airflow workers we should define env vars:
* `WORKERS_XCHNG_FOLDER` - this folder should be on NFS if we have a number
of workers on separate machines. We use this folder to share big files (megabytes)
between tasks.

## DBs

We create DB for ETL tasks on the same server as airflow DB
(postgres in `airflow-db`).
Add it to airflow env connection as `etl_db`.

And add to airflow env connection to some `dev DB` as `dev_db`.
Assuming this is business DB our ETL should work with. 

## Scaling workers

We can use `docker-compose` key `--scale` but better add more machines with workers.

### Testing airflow tasks
    export AIRFLOW_HOME=~/.airflow/
    export AIRFLOW__CORE__DAGS_FOLDER=$PWD/etl/
    airflow initdb  # init local SQLite DB
    airflow --help
