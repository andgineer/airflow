from datetime import datetime, timezone

import pytest
from airflow.models.dag import _run_task
from airflow.utils.state import State
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
    task = dag_hello_world.get_task('pandas_dataset')
    assert task is not None, 'Cannot find task pandas_dataset'
    assert task.upstream_task_ids == set(), 'pandas_dataset should not have upstream tasks'
    assert task.downstream_task_ids == {'merge'}, 'pandas_dataset should have merge as downstream task'

    with Session() as session:
        execution_date = datetime.now(tz=timezone.utc)
        dag_run = dag_hello_world.create_dagrun(
            run_id=f"test_run_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            execution_date=execution_date,
            start_date=execution_date,
            state=State.RUNNING,
            external_trigger=False,
            session=session,
        )

        # todo: simplify with BackfillJob
        tasks = dag_hello_world.task_dict
        while dag_run.state == State.RUNNING:
            schedulable_tis, _ = dag_run.update_state(session=session)
            for ti in schedulable_tis:
                ti.task = tasks[ti.task_id]
                _run_task(ti, session=session)

        task_instance = dag_run.get_task_instance(task.task_id)
        assert task_instance.state == State.SUCCESS

        # Retrieve the result from XCom
        result = task_instance.xcom_pull(key='return_value', task_ids=task.task_id)
        assert result == 'Pandas', f'pandas_dataset returned {result} instead of Pandas'
