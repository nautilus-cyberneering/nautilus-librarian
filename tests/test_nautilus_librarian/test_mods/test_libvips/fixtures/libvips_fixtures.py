import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def libvips_fixtures_dir():
    return os.path.dirname(Path(__file__).resolve())
