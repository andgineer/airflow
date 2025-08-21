from psycopg2.extensions import connection  # pylint: disable=import-error

from airflow.providers.postgres.hooks.postgres import PostgresHook  # pylint: disable=import-error,no-name-in-module


def get_session(conn_id: str) -> connection:
    """Get a PostgreSQL connection."""
    # Note: This function returns a raw psycopg2 connection, not a SQLAlchemy session
    hook = PostgresHook(postgres_conn_id=conn_id)
    return hook.get_conn()
