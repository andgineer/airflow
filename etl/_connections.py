import logging
from typing import Iterable, List

from sqlalchemy import and_

from airflow import settings
from airflow.models import Connection  # pylint: disable=ungrouped-imports

log = logging.getLogger()

DB_CONN_PREFIX = "db_"
FILE_PREFIX = "file_"


def conn_id_to_name(conn_id: str) -> str:
    """Extract DB name from Airflow Connection name.

    'db_dev' -> 'dev'
    """
    return "_".join(conn_id.split("_")[1:])


def dbs_to_update() -> List[str]:
    """Airflow Connections with conn_id started with `DB_CONN_PREFIX`."""
    session = settings.Session()
    try:
        conns: Iterable[Connection] = (
            session.query(Connection.conn_id)
            .filter(Connection.conn_id.ilike(f"{DB_CONN_PREFIX}%"))
            .all()
        )
        conn_ids = [conn.conn_id for conn in conns]
    except Exception:
        conn_ids = []
    finally:
        session.commit()
    return conn_ids


def files_conns(conn_type: str) -> Iterable[Connection]:
    """Airflow Connections with conn_id started with `FILE_PREFIX` and specific `conn_type`."""
    session = settings.Session()
    try:
        conns: Iterable[Connection] = (
            session.query(Connection)
            .filter(
                and_(
                    Connection.conn_id.ilike(f"{FILE_PREFIX}%"),
                    Connection.conn_type == conn_type,
                )
            )
            .all()
        )
    except Exception:
        conns = []
    finally:
        session.commit()
    return conns


def files_conn_ids(conn_type: str) -> List[str]:
    """Airflow Connection IDs with conn_id started with `FILE_PREFIX` and specific `conn_type`."""
    conns = files_conns(conn_type)
    return [conn.conn_id for conn in conns]


def files_folders(conn_type: str) -> List[str]:
    """Airflow Connections with conn_id started with `FILE_PREFIX` and specific `conn_type`."""
    conns = files_conns(conn_type)
    result = []
    for conn in conns:
        path = conn.extra_dejson.get("path", None)
        print(f"File connection {conn.conn_id}: {path}")
        if path is not None:
            result.append(path)
    return result
