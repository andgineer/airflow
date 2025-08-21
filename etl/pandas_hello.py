from datetime import timedelta
from logging import getLogger
from typing import Any

from _default import default_args

from airflow import DAG
from airflow.models.taskinstance import TaskInstance
from airflow.providers.standard.operators.python import PythonOperator

log = getLogger(__name__)

dag = DAG(  # pylint: disable=unexpected-keyword-arg
    "HelloPandas",
    default_args=default_args,
    description="Airflow+Anaconda -> perfect marriage",
    schedule=timedelta(days=1),
)


def word_dataset_task(  # pylint: disable=unused-argument
    task_instance: TaskInstance,
    word: str,
    **kwargs: Any,
) -> str:
    """Print the word and return it."""
    log.info("word_dataset_task got `%s`", word)
    return word


def merge_task(  # pylint: disable=unused-argument
    task_instance: TaskInstance,
    **kwargs: Any,
) -> Any:
    """Merge the two datasets."""
    result = task_instance.xcom_pull(task_ids=["hello_dataset", "pandas_dataset"])
    log.info("merge_task emit `%s`", result)
    return result


pandas_dataset = PythonOperator(
    dag=dag,
    task_id="pandas_dataset",
    python_callable=word_dataset_task,
    op_kwargs={"word": "Pandas"},
)
hello_dataset = PythonOperator(
    dag=dag,
    task_id="hello_dataset",
    python_callable=word_dataset_task,
    op_kwargs={"word": "Hello"},
)
merge = PythonOperator(
    dag=dag,
    task_id="merge",
    python_callable=merge_task,
)

[pandas_dataset, hello_dataset] >> merge  # pylint: disable=pointless-statement
