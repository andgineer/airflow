import pytest
from _config import Config


class TestConfig(Config):
    dags_folder = 'etl'  # relative to project root where we run pytest


@pytest.fixture
def config():
    return TestConfig()
