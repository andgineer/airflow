from airflow.providers.postgres.hooks.postgres import (  # pyrefly: ignore[missing-import]
    PostgresHook,  # pylint: disable=import-error,no-name-in-module
)
from psycopg2.extensions import (  # pyrefly: ignore[missing-import,missing-source-for-stubs]
    connection,  # pylint: disable=import-error
)


def get_session(conn_id: str) -> connection:
    """Get a PostgreSQL connection."""
    # Note: This function returns a raw psycopg2 connection, not a SQLAlchemy session
    hook = PostgresHook(postgres_conn_id=conn_id)
    return hook.get_conn()
