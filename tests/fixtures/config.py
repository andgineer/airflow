import pytest
from airflow import models
from airflow.utils.db import resetdb


from _config import Config


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



