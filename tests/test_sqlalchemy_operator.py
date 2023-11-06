import pytest
from unittest.mock import patch, MagicMock
from airflow.models import DAG
from datetime import datetime
from operators.sqlalchemy_operator import SQLAlchemyOperator

# Constants for the tests
DEFAULT_DATE = datetime(2021, 1, 1)
TEST_DAG_ID = 'unit_test_dag'


@pytest.fixture
def dag():
    return DAG(
        dag_id=TEST_DAG_ID,
        default_args={'owner': 'airflow', 'start_date': DEFAULT_DATE},
        schedule_interval='@daily',
    )


def test_sqlalchemy_operator_initialization(dag):
    conn_id = 'my_postgres_conn'
    test_callable = MagicMock()
    task = SQLAlchemyOperator(
        task_id='test_sql_task',
        conn_id=conn_id,
        python_callable=test_callable,
        dag=dag,
    )

    assert task.conn_id == conn_id
    assert task.python_callable is test_callable


@patch('operators.sqlalchemy_operator.get_session')
def test_sqlalchemy_operator_execute_success(mock_get_session, dag):
    session = MagicMock()
    mock_get_session.return_value = session

    def test_callable(session, **kwargs):
        return 'callable_success'

    task = SQLAlchemyOperator(
        task_id='test_sql_task',
        conn_id='my_postgres_conn',
        python_callable=test_callable,
        dag=dag,
    )

    result = task.execute(context={})
    session.commit.assert_called_once()
    session.rollback.assert_not_called()
    assert result == 'callable_success'


@patch('operators.sqlalchemy_operator.get_session')
def test_sqlalchemy_operator_execute_exception(mock_get_session, dag):
    session = MagicMock()
    mock_get_session.return_value = session

    def test_callable(session, **kwargs):
        raise Exception("Error in the callable")

    task = SQLAlchemyOperator(
        task_id='test_sql_task',
        conn_id='my_postgres_conn',
        python_callable=test_callable,
        dag=dag,
    )

    with pytest.raises(Exception) as e:
        task.execute(context={})
    assert str(e.value) == "Error in the callable"
    session.commit.assert_not_called()
    session.rollback.assert_called_once()
