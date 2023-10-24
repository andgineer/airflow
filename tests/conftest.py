import os.path
import os
import sys
import logging
from pathlib import Path
import modules_load


log = logging.getLogger()

script_dir = os.path.dirname(os.path.abspath(__file__))
airflow_home = os.path.join(script_dir, 'airflow_home')
etl_dir = os.path.join(script_dir, '..', 'etl')

sys.path.append(etl_dir)  # make Python 1st look for packages in ETL dir
os.environ['AIRFLOW__CORE__DAGS_FOLDER'] = etl_dir
os.environ['AIRFLOW_HOME'] = airflow_home
os.environ['AIRFLOW_CONFIG'] = os.path.join(airflow_home, 'airflow_test.cfg')

# load Airflow only after setting Airflow env vars
modules_load.asterisk(Path(__file__).parent / 'fixtures', 'fixtures', globals())
