"""SQLite engine, session factory, and the FastAPI session dependency."""

from collections.abc import Iterator
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings

_settings = get_settings()


def _ensure_sqlite_dir(url: str) -> None:
    """SQLite will not create missing parent directories; do it for it."""
    prefix = "sqlite:///"
    if url.startswith(prefix):
        path = Path(url[len(prefix) :])
        if str(path) != ":memory:":
            path.parent.mkdir(parents=True, exist_ok=True)


_ensure_sqlite_dir(_settings.database_url)

engine: Engine = create_engine(
    _settings.database_url,
    connect_args={"check_same_thread": False},
    future=True,
)


@event.listens_for(Engine, "connect")
def _set_sqlite_pragmas(dbapi_connection: object, _connection_record: object) -> None:
    """Foreign keys are off by default in SQLite; WAL keeps reads fast during writes."""
    cursor = dbapi_connection.cursor()  # type: ignore[attr-defined]
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()


SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


def get_db() -> Iterator[Session]:
    """FastAPI dependency yielding a request-scoped session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]
"""Use this in route signatures: `def view(db: DbSession) -> ...`."""
