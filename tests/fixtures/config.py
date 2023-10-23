import os

import pytest
from airflow.utils.dates import days_ago
from airflow import models, settings
from airflow.utils.db import initdb
from airflow.utils import db as airflow_db


from _config import Config

pytest_plugins = ["helpers_namespace"]


class TestConfig(Config):
    dags_folder = 'etl'  # relative to project root where we run pytest


@pytest.fixture(scope='session')
def config():
    os.environ['AIRFLOW_CONFIG'] = 'tests/resources/airflow_test.cfg'
    airflow_db.resetdb()
    initdb()

    return TestConfig()


@pytest.fixture(scope='session')
def dag_bag(dag_files):
    dag_bag = models.DagBag(include_examples=False)
    for file_name in dag_files:
        dag_bag.process_file(file_name, only_if_updated=False)
    return dag_bag


@pytest.fixture
def dag_hello_world(dag_bag):
    result = dag_bag.get_dag('HelloPandas')
    return result




