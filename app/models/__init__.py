"""Importing this package registers every table on Base.metadata (Alembic relies on that)."""

from app.models.base import Base, CitationMixin, TimestampMixin, utcnow
from app.models.content import (
    DocumentRequirement,
    Faq,
    MilestoneTemplate,
    Scheme,
    SchemeTrack,
    SourceDocument,
)
from app.models.enums import (
    ApplicationStatus,
    Confidence,
    DocumentStatus,
    MilestoneStatus,
    SchemeStatus,
    TriggerType,
)
from app.models.tracker import (
    ActivityLog,
    Application,
    Company,
    DocumentInstance,
    Lead,
    MilestoneInstance,
    User,
)

__all__ = [
    "ActivityLog",
    "Application",
    "ApplicationStatus",
    "Base",
    "CitationMixin",
    "Company",
    "Confidence",
    "DocumentInstance",
    "DocumentRequirement",
    "DocumentStatus",
    "Faq",
    "Lead",
    "MilestoneInstance",
    "MilestoneStatus",
    "MilestoneTemplate",
    "Scheme",
    "SchemeStatus",
    "SchemeTrack",
    "SourceDocument",
    "TimestampMixin",
    "TriggerType",
    "User",
    "utcnow",
]
