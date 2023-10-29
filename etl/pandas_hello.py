from datetime import timedelta
from typing import Any

from _default import default_args

from airflow import DAG
from airflow.models.taskinstance import TaskInstance
from airflow.operators.python import PythonOperator
from logging import getLogger

log = getLogger(__name__)

dag = DAG(
    "HelloPandas",
    default_args=default_args,
    description="Airflow+Anaconda -> perfect marriage",
    schedule_interval=timedelta(days=1),
)


def word_dataset_task(
    task_instance: TaskInstance, word: str, **kwargs  # pylint: disable=unused-argument
) -> str:
    """Print the word and return it."""
    log.info(f"word_dataset_task got `{word}`")
    return word


def merge_task(task_instance: TaskInstance, **kwargs) -> Any:  # pylint: disable=unused-argument
    """Merge the two datasets."""
    result = task_instance.xcom_pull(task_ids=["hello_dataset", "pandas_dataset"])
    log.info(f"merge_task emit `{result}`")
    return result


pandas_dataset = PythonOperator(
    dag=dag,
    task_id="pandas_dataset",
    python_callable=word_dataset_task,
    provide_context=True,
    op_kwargs={"word": "Pandas"},
)
hello_dataset = PythonOperator(
    dag=dag,
    task_id="hello_dataset",
    python_callable=word_dataset_task,
    provide_context=True,
    op_kwargs={"word": "Hello"},
)
merge = PythonOperator(
    dag=dag,
    task_id="merge",
    python_callable=merge_task,
    provide_context=True,
)

[pandas_dataset, hello_dataset] >> merge  # pylint: disable=pointless-statement
