import copy
import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture(autouse=True)
def snapshot_activities():
    """Snapshot and restore the in-memory activities before/after each test."""
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)


@pytest.fixture
def client():
    """Provide a TestClient instance for the FastAPI app."""
    with TestClient(app_module.app) as c:
        yield c
