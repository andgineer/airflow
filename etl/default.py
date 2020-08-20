from datetime import datetime
from airflow.models import Variable


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 8, 16),
    'email': ['andrey@sorokin.engineer'],
    'email_on_failure': True,
}


def dbs_to_update():
    # todo remove "KeyError: 'Variable dbs_to_update does not exist'"
    # The error happens during airflow initdb when we did not created the variable yet.
    # We cannot create the variable before initdb because we need DB to create it %-(
    # I do not want to suppress the error because I want it to indicate if the DAG cannot run.
    # Why DB migrations load (and run!) DAGs at all?!
    # May be we can understand that we are in initdb mode? But we need to load DAG also in Worker..
    # The error happens only at Airflow DB creation. Just ignore it for the moment.
    yield from Variable.get('dbs_to_update').split(',')
