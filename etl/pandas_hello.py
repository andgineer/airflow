from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.taskinstance import TaskInstance
from datetime import timedelta
from _default import default_args


dag = DAG(
    'HelloPandas',
    default_args=default_args,
    description='Airflow+Anaconda -> perfect marriage',
    schedule_interval=timedelta(days=1),
)


def word_dataset_task(task_instance: TaskInstance, word: str, **kwargs):
    return word


def merge_task(task_instance: TaskInstance, **kwargs):
    return task_instance.xcom_pull(task_ids=['hello_dataset', 'pandas_dataset'])


pandas_dataset = PythonOperator(
    dag=dag,
    task_id='pandas_dataset',
    python_callable=word_dataset_task,
    provide_context=True,
    op_kwargs={'word': 'Pandas'},
)
hello_dataset = PythonOperator(
    dag=dag,
    task_id='hello_dataset',
    python_callable=word_dataset_task,
    provide_context=True,
    op_kwargs={'word': 'Hello'},
)
merge = PythonOperator(
    dag=dag,
    task_id='merge',
    python_callable=merge_task,
    provide_context=True,
)

[pandas_dataset, hello_dataset] >> merge
