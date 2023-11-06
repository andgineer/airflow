[![CI status](https://github.com/andgineer/airflow/workflows/ci/badge.svg)](https://github.com/andgineer/airflow/actions)
[![Coverage](https://raw.githubusercontent.com/andgineer/airflow/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/andgineer/airflow/blob/python-coverage-comment-action-data/htmlcov/index.html)
# Apache Airflow + Anaconda

Docker-compose environment for local debugging Apache Airflow DAGs.

With local Airflow scheduler and workers, DB and live reload of DAGs.

Minicoda already installed, so you can use any machine learning or data-science
package from Anaconda in your ETL pipelines.

[Apache Airflow](https://airflow.apache.org/docs/stable/) is a workflow management platform.
This makes it easier to build data pipelines, monitor them, and perform ETL operations.

Airflow pipelines are configuration as Python code, allowing for dynamic pipeline
generation.

Apache Airflow provides you [WebUI](https://airflow.apache.org/docs/stable/ui.html)
and [command-line interface](https://airflow.apache.org/docs/stable/usage-cli.html).

## How to run

    ./compose.sh build
    ./up.sh

Airflow: http://127.0.0.1:8080/home (user admin, password admin)
Flower: http://127.0.0.1:5551

ETL tasks (DAGs) are in `etl/`. They mounted into Airflow containers so all your
changes live update your DAGs.

## DUGs

I created demo-DAG `HelloPandas` so you can see that everything is working.
In the `merge` task logs you should see `Done. Returned value was: ('Hello', 'Pandas')`.

## DBs

We create DB for ETL tasks on the same server as airflow DB
(postgres in `airflow-db`).
Add it to airflow env connection as `etl_db`.

And add to airflow env connection to some `dev DB` as `db_dev`.
Assuming this is business DB our ETL should work with.

## Scaling workers

We can use `docker-compose` key `--scale` but better add more machines with workers.

## Email
To send emails from Airflow you need to configure SMTP server in `airflow.cfg` file.

### Testing airflow tasks

#### Create virtual environment
    . ./activate.sh

#### Run tests
    pytest

### Create migration script for ETL DB

Describe your SQLAlchemy objects in `etl/db/models`.
All models should inherits from `db.models.Base`.

```console
# compare DB models and current ETL DB and create DB upgrade script in alembic/versions
./alembic.sh revision --autogenerate -m \"Schema changes.\"

# apply script to the DB so after that DB meta data will reflect DB models
./alembic.sh upgrade head
```
