from datetime import datetime
from airflow.models import Connection
from airflow import settings
from typing import Iterable


DB_CONN_PREFIX='db_'

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 8, 16),
    'email': ['andrey@sorokin.engineer'],
    'email_on_failure': True,
}


def dbs_to_update():
    """
    Airflow Connections with conn_id started with `BB_DB_CONN_PREFIX`
    """
    session = settings.Session()
    conns: Iterable[Connection] = (
        session.query(Connection.conn_id)
        .filter(Connection.conn_id.ilike(f'{DB_CONN_PREFIX}%'))
        .all()
    )
    return [conn.conn_id for conn in conns]
