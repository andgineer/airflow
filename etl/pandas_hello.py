from datetime import timedelta

from _default import default_args

from airflow import DAG
from airflow.models.taskinstance import TaskInstance
from airflow.operators.python import PythonOperator

dag = DAG(
    "HelloPandas",
    default_args=default_args,
    description="Airflow+Anaconda -> perfect marriage",
    schedule_interval=timedelta(days=1),
)


def word_dataset_task(task_instance: TaskInstance, word: str, **kwargs):
    """Print the word and return it"""
    return word


def merge_task(task_instance: TaskInstance, **kwargs):
    """Merge the two datasets"""
    return task_instance.xcom_pull(task_ids=["hello_dataset", "pandas_dataset"])


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

[pandas_dataset, hello_dataset] >> merge
