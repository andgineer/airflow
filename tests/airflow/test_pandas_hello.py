from datetime import datetime, timezone

import pytest
from airflow.utils.state import DagRunState, TaskInstanceState
from airflow.settings import Session
from airflow.utils.dag_cycle_tester import check_cycle

format_string = '%Y-%m-%dT%H:%M:%SZ'


def test_dags_load_with_no_errors(dag_bag):
    if dag_bag.dag_ids:
        for dag_id in dag_bag.dag_ids:
            dag_obj = dag_bag.get_dag(dag_id)
            assert dag_obj is not None, f'Cannot load DAG {dag_id}'
            assert len(dag_obj.tasks) > 0, f'DAG {dag_id} has no tasks'
            check_cycle(dag_obj)  # check for cycles
    else:
        pytest.fail(f"No DAGs: {dag_bag.import_errors}")


def test_pandas_dataset_task(dag_bag):
    dag_hello_world = dag_bag.get_dag('HelloPandas')

    task_pandas = dag_hello_world.get_task('pandas_dataset')
    assert task_pandas is not None, 'Cannot find task pandas_dataset'
    assert task_pandas.upstream_task_ids == set(), 'pandas_dataset should not have upstream tasks'
    assert task_pandas.downstream_task_ids == {'merge'}, 'pandas_dataset should have merge as downstream task'

    task_hello = dag_hello_world.get_task('hello_dataset')
    assert task_hello is not None, 'Cannot find task hello_dataset'
    assert task_hello.upstream_task_ids == set(), 'hello_dataset should not have upstream tasks'
    assert task_hello.downstream_task_ids == {'merge'}, 'hello_dataset should have merge as downstream task'

    task_merge = dag_hello_world.get_task('merge')
    assert task_merge is not None, 'Cannot find task merge'
    assert task_merge.upstream_task_ids == {'pandas_dataset', 'hello_dataset'}, 'merge should have pandas_dataset and hello_dataset as upstream tasks'
    assert task_merge.downstream_task_ids == set(), 'merge should not have downstream tasks'

    # Test individual tasks using direct execution (Airflow v3 approach)
    
    # Test pandas_dataset task directly
    # Create a mock context for testing
    mock_context = {
        'task_instance': None,  # Will be set by the test framework
        'logical_date': datetime.now(tz=timezone.utc),
        'ds': datetime.now(tz=timezone.utc).strftime('%Y-%m-%d'),
    }
    
    # For PythonOperator tasks, we can test the python_callable directly
    result_pandas = task_pandas.python_callable(
        task_instance=None,  # Not needed for this simple test
        word='Pandas'
    )
    assert result_pandas == 'Pandas', f'pandas_dataset returned {result_pandas} instead of Pandas'
    
    # Test hello_dataset task  
    result_hello = task_hello.python_callable(
        task_instance=None,  # Not needed for this simple test
        word='Hello'
    )
    assert result_hello == 'Hello', f'hello_dataset returned {result_hello} instead of Hello'
