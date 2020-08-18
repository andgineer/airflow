import pytest
from pathlib import Path
from tests.fixtures.config import TestConfig
from typing import List


@pytest.fixture
def dag_files(config: TestConfig) -> List[Path]:
    return list(Path(config.dags_folder).glob('*.py'))
