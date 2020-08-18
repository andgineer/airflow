import pytest
from cdf_config import Config


class TestConfig(Config):
    dags_folder = 'etl'  # relative to project root where we run pytest


@pytest.fixture
def config():
    return TestConfig()
