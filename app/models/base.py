"""Declarative base and small column mixins shared across models."""

from datetime import UTC, date, datetime

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.models.enums import Confidence


def utcnow() -> datetime:
    """Timezone-aware UTC now; stored naive-free so exports are unambiguous."""
    return datetime.now(UTC)


class Base(DeclarativeBase):
    """Common declarative base for every table."""


class TimestampMixin:
    """created_at / updated_at maintained by the ORM, not by triggers."""

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class CitationMixin:
    """Every seeded fact must carry provenance. The loader rejects records missing these."""

    source_title: Mapped[str] = mapped_column(String(500))
    source_url: Mapped[str] = mapped_column(String(1000))
    source_date: Mapped[date]
    clause_ref: Mapped[str] = mapped_column(String(200))
    retrieved_on: Mapped[date]
    confidence: Mapped[Confidence] = mapped_column(
        Enum(Confidence, native_enum=False, validate_strings=True),
        default=Confidence.needs_review,
    )
