from psycopg2.extensions import connection

from airflow.providers.postgres.hooks.postgres import PostgresHook


def get_session(conn_id: str) -> connection:
    """Get a SQLAlchemy session."""
    hook = PostgresHook(postgres_conn_id=conn_id)
    return hook.get_conn()
