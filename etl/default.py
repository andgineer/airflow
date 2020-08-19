from datetime import datetime


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 8, 16),
    'email': ['andrey@sorokin.engineer'],
    'email_on_failure': True,
}

dbs_to_update = ['dev_db']
