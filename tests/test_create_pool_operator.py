import pytest
from unittest.mock import patch, MagicMock

from airflow.exceptions import PoolNotFound
from airflow.models import DAG, Pool
from operators.create_pool import CreatePoolOperator
from datetime import datetime

@patch('operators.create_pool.get_pool')
@patch('operators.create_pool.create_pool')
def test_create_pool(mock_create_pool, mock_get_pool, dag):
    mock_get_pool.side_effect = PoolNotFound
    mock_create_pool.return_value = Pool(pool='test_pool', slots=10, description='Test pool')

    operator = CreatePoolOperator(
        task_id='create_pool',
        name='test_pool',
        slots=10,
        description='Test pool',
        dag=dag,
    )

    operator.execute(context={})

    mock_create_pool.assert_called_once_with(name='test_pool', slots=10, description='Test pool')


@patch('operators.create_pool.get_pool')
@patch('operators.create_pool.create_pool')
def test_do_not_create_pool_if_exists(mock_create_pool, mock_get_pool, dag):
    mock_get_pool.return_value = Pool(pool='test_pool', slots=10, description='Test pool')

    operator = CreatePoolOperator(
        task_id='create_pool',
        name='test_pool',
        slots=10,
        description='Test pool',
        dag=dag,
    )

    operator.execute(context={})

    mock_create_pool.assert_not_called()
