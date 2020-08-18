from datetime import datetime


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 8, 16),
    'email': ['andrey@sorokin.engineer'],
    'email_on_failure': True,
    # 'catchup': False,  # do not auto-run for all missed dates
}

dbs_to_update = ['dev_db']
