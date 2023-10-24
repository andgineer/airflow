import os.path
import os
import sys
import logging
from pathlib import Path
import modules_load


log = logging.getLogger()

sys.path.append(os.path.join(os.path.dirname(__file__), '../etl'))
os.environ['AIRFLOW__CORE__DAGS_FOLDER'] = './etl'
os.environ['AIRFLOW_HOME'] = './tests/airflow_home'
os.environ['AIRFLOW_CONFIG'] = 'tests/resources/airflow_test.cfg'

# load Airflow only after setting AIRFLOW_HOME and Dags folder
modules_load.asterisk(Path(__file__).parent / 'fixtures', 'fixtures', globals())
