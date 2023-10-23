import pytest
from pathlib import Path
from fixtures.config import TestConfig
from typing import List


NON_DAG_FILE_PREFIX = '_'


@pytest.fixture(scope='session')
def dag_files(config: TestConfig) -> List[str]:
    return [
        str(Path(file_path).relative_to(config.dags_folder))
        for file_path in Path(config.dags_folder).glob('*.py')
        if not Path(file_path).name.startswith(NON_DAG_FILE_PREFIX)
    ]
