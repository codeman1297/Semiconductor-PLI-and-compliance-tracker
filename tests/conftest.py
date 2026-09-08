"""Test fixtures. Each test module gets a throwaway SQLite file, never the dev database."""

import os
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest

_TMP_DB = Path(tempfile.gettempdir()) / "incentive_tracker_test.db"
os.environ.setdefault("DATABASE_URL", f"sqlite:///{_TMP_DB}")
os.environ.setdefault("SECRET_KEY", "test-key")

from fastapi.testclient import TestClient  # noqa: E402

from app.db import engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Base  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _schema() -> Iterator[None]:
    """Create the schema from the models, then drop it. Migrations are tested separately."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
