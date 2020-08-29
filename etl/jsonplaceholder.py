"""
You can set date to request in manual run from Airflow WebUI
('Configuration JSON (Optional)'):
    {"date": "2020-08-03"}
"""
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models.taskinstance import TaskInstance
# from airflow.utils.helpers import cross_downstream
import jsonplaceholder
from datetime import datetime, timedelta, timezone
from _default import default_args, dbs_to_update


dag = DAG(
    dag_id='jsonplaceholder',
    schedule_interval='0 2 * * *',  # daily at 2:00 AM
    default_args=default_args,
)


def jsonplaceholder_download(task_instance: TaskInstance, days_from_now: int, **kwargs):
    try:
        manual_date = '{{ dag_run.conf["date"] }}'
        download_date = datetime.strptime(manual_date, '%Y-%m-%d')
    except ValueError:
        download_date = datetime.now(
            tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0
                                     ) - timedelta(days=days_from_now)
    result = jsonplaceholder.download(download_date)
    print(f'Got {len(result)} rows')
    return f'file_{task_instance.task_id}.txt'


def tsv_upload(task_instance: TaskInstance, conn_id, **kwargs):
    print('Files from upstream tasks:', task_instance.xcom_pull())
    # hook = PostgresHook(postgres_conn_id=conn_id)
    # cursor = hook.get_conn().cursor()
    # cursor.execute('SELECT name FROM "??"')
    # print(cursor.fetchall())


downloaders = [
    PythonOperator(
        dag=dag,
        task_id=f'download_{day}',
        python_callable=jsonplaceholder_download,
        task_concurrency=3,  # Do not DOS jsonplaceholder
        provide_context=True,
        op_kwargs={'days_from_now': day},
    )
    for day in range(7)
]

for downloader in downloaders:
    downloader >> [
        PythonOperator(
            dag=dag,
            task_id=f'upload_to__{db_to_update}',
            python_callable=tsv_upload,
            provide_context=True,
            op_kwargs={'conn_id': db_to_update},
        )
        for db_to_update in dbs_to_update()
    ]
