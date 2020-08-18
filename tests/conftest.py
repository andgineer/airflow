import os.path
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '../etl'))

import modules_load
import logging
from pathlib import Path

modules_load.asterisk(Path(__file__).parent / 'fixtures', 'fixtures', globals())

log = logging.getLogger()
