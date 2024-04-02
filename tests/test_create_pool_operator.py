import pytest
from unittest.mock import patch, MagicMock
from airflow.models import Pool
from operators.create_pool import CreatePoolOperator


@patch('operators.create_pool.create_session')
def test_create_pool(mock_create_session, dag):
    mock_session = MagicMock()
    mock_create_session.return_value.__enter__.return_value = mock_session
    mock_session.query.return_value.filter.return_value.first.return_value = None

    operator = CreatePoolOperator(
        task_id='create_pool',
        name='test_pool',
        slots=10,
        description='Test pool',
        dag=dag,
    )
    operator.execute(context={})

    expected_pool = Pool(pool='test_pool', slots=10, description='Test pool')
    call_args = mock_session.add.call_args[0][0]
    assert call_args.pool == expected_pool.pool
    assert call_args.slots == expected_pool.slots
    assert call_args.description == expected_pool.description
    mock_session.commit.assert_called_once()


@patch('operators.create_pool.create_session')
def test_do_not_create_pool_if_exists(mock_create_session, dag):
    mock_session = MagicMock()
    mock_create_session.return_value.__enter__.return_value = mock_session
    mock_session.query.return_value.filter.return_value.first.return_value = Pool(pool='test_pool', slots=10, description='Test pool')

    operator = CreatePoolOperator(
        task_id='create_pool',
        name='test_pool',
        slots=10,
        description='Test pool',
        dag=dag,
    )
    operator.execute(context={})

    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()