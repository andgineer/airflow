from typing import Any

from sqlalchemy.orm import Session, sessionmaker

from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.decorators import apply_defaults


def get_session(conn_id: str) -> Session:
    """Get SQLAlchemy session."""
    hook = PostgresHook(postgres_conn_id=conn_id)
    engine = hook.get_sqlalchemy_engine()
    return sessionmaker(bind=engine)()


class SQLAlchemyOperator(PythonOperator):  # type: ignore
    """PythonOperator with SQLAlchemy session management.

    Creates session for the Python callable
    and commit/rollback it afterward.

    Set `conn_id` with you DB connection.

    Pass `session` parameter to the python callable.
    """

    @apply_defaults  # type: ignore
    def __init__(self, conn_id: str, *args: Any, **kwargs: Any) -> None:
        """Init."""
        self.conn_id = conn_id
        super().__init__(*args, **kwargs)

    def execute_callable(self) -> Any:
        """Execute callable with SQLAlchemy session management."""
        session = get_session(self.conn_id)
        try:
            result = self.python_callable(*self.op_args, session=session, **self.op_kwargs)
        except Exception:
            session.rollback()
            raise
        session.commit()
        return result
