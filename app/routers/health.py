"""Liveness and readiness endpoints for the container platform."""

from typing import Literal

from fastapi import APIRouter
from sqlalchemy import text

from app.db import DbSession

router = APIRouter(tags=["ops"])


@router.get("/healthz")
def healthz() -> dict[str, Literal["ok"]]:
    """Process is up. No database touched, so this stays cheap."""
    return {"status": "ok"}


@router.get("/readyz")
def readyz(db: DbSession) -> dict[str, str]:
    """Process is up and the database answers."""
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}
