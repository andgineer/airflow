# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Docker-compose based Apache Airflow 3 development environment with Anaconda/Miniconda integration for local debugging of ETL DAGs. The setup includes a local Airflow scheduler, Celery workers, PostgreSQL database, Redis broker, and live reload of DAGs.

## Architecture

### Core Components

- **etl/**: Contains all Airflow DAGs and ETL logic
  - DAG files are placed directly in `etl/` (e.g., `pandas_hello.py`)
  - Non-DAG files must be prefixed with `_` (e.g., `_config.py`, `_connections.py`, `_default.py`)
  - `etl/operators/`: Custom Airflow operators
  - `etl/db/`: Database models and session management
  - `etl/plugins/`: Airflow plugins

- **docker/**: Docker configurations
  - `docker/airflow/`: Main Airflow container (webserver, scheduler, Celery Flower)
  - `docker/airflow-worker/`: Celery worker container
  - `docker/airflow-db/`: PostgreSQL database container

- **tests/**: Test suite with fixtures
  - Uses custom `conftest.py` that sets up Airflow environment variables
  - Test fixtures in `tests/fixtures/`
  - Tests must import DAGs from `etl/` directory

- **alembic/**: Database migration scripts for ETL database (not Airflow metadata DB)

### Connection Management

The codebase uses a naming convention for Airflow Connections:
- `db_*`: Database connections (e.g., `db_dev`, `etl_db`)
- `file_*`: File-based connections with paths in `extra_dejson`

Connection utilities in `etl/_connections.py`:
- `dbs_to_update()`: Returns all DB connections with `db_` prefix
- `files_conns(conn_type)`: Returns file connections by type
- `conn_id_to_name(conn_id)`: Extracts name from connection ID

### Custom Operators

- **CreatePoolOperator** (`etl/operators/create_pool.py`): Creates Airflow pools if they don't exist
- **SQLAlchemyOperator** (`etl/operators/sqlalchemy_operator.py`): PythonOperator with automatic SQLAlchemy session management (commit/rollback)

### Database Models

SQLAlchemy models should be placed in `etl/db/models/` and inherit from `etl.db.models.Base`.

## Development Commands

### Environment Setup

```bash
# Create/activate conda environment with Airflow 3 and dependencies
. ./activate.sh
```

This creates a conda environment named "airflow" with Python 3.12 and installs all required dependencies including Airflow from conda-forge.

### Running Airflow

```bash
# Build Docker images
./compose.sh build

# Start all services (DB, broker, Airflow webserver, scheduler, workers)
./up.sh

# Start specific service
./up.sh airflow-db

# Stop services
./stop.sh
```

Access points:
- Airflow UI: http://127.0.0.1:8080/home (admin/admin)
- Celery Flower: http://127.0.0.1:5551

### Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_connections.py

# Run with coverage
pytest -v --cov=etl tests/
```

Tests use a custom Airflow environment configured in `tests/conftest.py` that points to `tests/airflow_home/` and loads DAGs from `etl/`.

### Code Quality

```bash
# Run pre-commit hooks manually
pre-commit run --all-files

# Type checking (mypy with strict mode)
mypy --strict --ignore-missing-imports etl/

# Linting (pylint with max line length 99)
pylint --max-line-length=99 etl/
```

Pre-commit hooks run ruff (formatter + linter), mypy, and pylint automatically.

### Database Migrations

```bash
# Create migration for ETL database (compares models in etl/db/models/ with current DB)
./alembic.sh revision --autogenerate -m "Schema changes."

# Apply migrations
./alembic.sh upgrade head

# View migration history
./alembic.sh history
```

Alembic commands run inside the Airflow Docker container. The script automatically detects if containers are running and uses `exec` or `run` accordingly.

### Database Access

```bash
# Access ETL database via psql
./psql.sh

# Dump database
./dump_db.sh

# Kill database container
./kill-db.sh
```

### Docker Utilities

```bash
# Execute commands in running container
./exec.sh <service-name> <command>

# Run one-off command in new container
./run.sh <service-name> <command>
```

## Key Conventions

1. **DAG Files**: Place DAGs directly in `etl/`, prefix utility files with `_`
2. **Default DAG Args**: Import from `etl._default` for consistent default_args
3. **Connection Naming**: Use `db_*` for databases, `file_*` for file paths
4. **SQLAlchemy Models**: Inherit from `etl.db.models.Base`
5. **Session Management**: Use `SQLAlchemyOperator` for automatic session handling
6. **Python Version**: 3.12 (sync with CI configuration)
7. **Airflow Version**: Currently using Airflow 3.0.4 (check `.github/workflows/ci.yml` and `activate.sh`)

## Environment Variables

The project uses environment variables exported via `export_vars.sh`:
- Database connection URLs: `DEV_DB_URL`, `ETL_DB_URL`, `AIRFLOW_DB_URL`
- Airflow Fernet key: `AIRFLOW_FERNET_KEY`
- Proxy settings: `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`
- Worker exchange folder: `WORKERS_XCHNG_FOLDER`

Configuration is accessed via `etl._config.Config` singleton.

## Testing Considerations

- Tests set `AIRFLOW_HOME` to `tests/airflow_home/`
- Tests set `AIRFLOW__CORE__DAGS_FOLDER` to `etl/`
- ETL directory is added to Python path in test setup
- Use `modules_load` helper to dynamically load test fixtures
