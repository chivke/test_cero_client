import os

import pytest


@pytest.fixture
def dentalink_token() -> str:
    return os.environ.get("DENTALINK_TOKEN", "")
