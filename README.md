[![CI status](https://github.com/andgineer/airflow/workflows/ci/badge.svg)](https://github.com/andgineer/airflow/actions)
[![Coverage](https://raw.githubusercontent.com/andgineer/airflow/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/andgineer/airflow/blob/python-coverage-comment-action-data/htmlcov/index.html)
# Apache Airflow 3 + Anaconda

Docker Compose environment for local debugging of Apache Airflow DAGs with live reload.

Includes Airflow scheduler, Celery workers, PostgreSQL database, and Miniconda for using machine learning and data science packages from Anaconda in your ETL pipelines.

[Apache Airflow](https://airflow.apache.org/docs/stable/) is a workflow management platform for building and monitoring data pipelines. Pipelines are configured as Python code, enabling dynamic pipeline generation.

## Quick Start

```bash
./compose.sh build
./up.sh
```

**Access:**
- Airflow UI: http://127.0.0.1:8080/home (username: `admin`, password: `admin`)
- Celery Flower: http://127.0.0.1:5551

DAGs are in `etl/` and mounted into containers for live updates.

## Demo DAG

The repository includes a demo DAG `HelloPandas` to verify everything works.
Check the `merge` task logs for: `Done. Returned value was: ('Hello', 'Pandas')`

## Database Connections

The environment creates a PostgreSQL database for ETL tasks (same server as Airflow metadata DB in `airflow-db` container).

**Required Airflow Connections:**
- `etl_db` - ETL tasks database
- `db_dev` - Development/business database for ETL operations

## Configuration

**Scaling Workers:** Use `docker-compose --scale` or deploy workers on separate machines.

**Email Notifications:** Configure SMTP server in `airflow.cfg`.

## Development

### Testing

```bash
# Create/activate conda environment
. ./activate.sh

# Run tests
pytest
```

### Database Migrations

Define SQLAlchemy models in `etl/db/models/` (inherit from `db.models.Base`).

```bash
# Generate migration script
./alembic.sh revision --autogenerate -m "Schema changes."

# Apply migrations
./alembic.sh upgrade head
```

## Coverage Reports
- [Codecov](https://app.codecov.io/gh/andgineer/airflow/tree/master/etl)
- [Coveralls](https://coveralls.io/github/andgineer/airflow)
