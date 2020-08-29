from sqlalchemy.orm import Session
from airflow.hooks.postgres_hook import PostgresHook


def get_session(conn_id: str) -> Session:
    hook = PostgresHook(postgres_conn_id=conn_id)
    cursor = hook.get_conn()
    return cursor
