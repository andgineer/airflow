from datetime import datetime

import pytest
from airflow import models
from airflow.models import DAG
from airflow.utils.db import resetdb

from _config import Config


DEFAULT_DATE = datetime(2021, 1, 1)
TEST_DAG_ID = 'unit_test_dag'


class TestConfig(Config):
    dags_folder = 'etl'  # relative to project root where we run pytest
    
    
@pytest.fixture(scope='session')
def config():
    resetdb()
    yield TestConfig()


@pytest.fixture(scope='session')
def dag_bag(dag_files):
    dag_bag = models.DagBag(include_examples=False)
    for file_name in dag_files:
        dag_bag.process_file(file_name, only_if_updated=False)
    return dag_bag


@pytest.fixture
def dag_hello_world(dag_bag):
    return dag_bag.get_dag('HelloPandas')


@pytest.fixture
def dag():
    return DAG(
        dag_id=TEST_DAG_ID,
        default_args={'owner': 'airflow', 'start_date': DEFAULT_DATE},
        schedule_interval='@daily',
    )
