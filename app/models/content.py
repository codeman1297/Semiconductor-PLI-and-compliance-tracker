"""Scheme content. Seeded from YAML in data/schemes/; the web app only reads these."""

from datetime import date

from sqlalchemy import Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CitationMixin, TimestampMixin
from app.models.enums import SchemeStatus, TriggerType


class Scheme(Base, TimestampMixin):
    """A government incentive scheme, e.g. ISM, DLI, ECMS, or a state scheme."""

    __tablename__ = "scheme"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(300))
    administering_body: Mapped[str] = mapped_column(String(300))
    status: Mapped[SchemeStatus] = mapped_column(
        Enum(SchemeStatus, native_enum=False, validate_strings=True)
    )
    summary_md: Mapped[str] = mapped_column(Text, default="")
    official_url: Mapped[str] = mapped_column(String(1000))
    last_reviewed_on: Mapped[date]

    tracks: Mapped[list["SchemeTrack"]] = relationship(
        back_populates="scheme", cascade="all, delete-orphan", order_by="SchemeTrack.code"
    )
    faqs: Mapped[list["Faq"]] = relationship(back_populates="scheme", cascade="all, delete-orphan")


class SchemeTrack(Base, TimestampMixin):
    """A sub-programme within a scheme: fab, ATMP/OSAT, compound semi, design-linked, etc."""

    __tablename__ = "scheme_track"
    __table_args__ = (UniqueConstraint("scheme_id", "code", name="uq_track_scheme_code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    scheme_id: Mapped[int] = mapped_column(ForeignKey("scheme.id", ondelete="CASCADE"), index=True)
    code: Mapped[str] = mapped_column(String(60))
    name: Mapped[str] = mapped_column(String(300))
    description_md: Mapped[str] = mapped_column(Text, default="")

    scheme: Mapped[Scheme] = relationship(back_populates="tracks")
    milestone_templates: Mapped[list["MilestoneTemplate"]] = relationship(
        back_populates="track",
        cascade="all, delete-orphan",
        order_by="MilestoneTemplate.sequence",
    )


class MilestoneTemplate(Base, TimestampMixin, CitationMixin):
    """One step in a track's disbursement sequence, as stated by the scheme documents."""

    __tablename__ = "milestone_template"
    __table_args__ = (UniqueConstraint("track_id", "sequence", name="uq_milestone_track_seq"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    track_id: Mapped[int] = mapped_column(
        ForeignKey("scheme_track.id", ondelete="CASCADE"), index=True
    )
    sequence: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(300))
    description_md: Mapped[str] = mapped_column(Text, default="")
    trigger_type: Mapped[TriggerType] = mapped_column(
        Enum(TriggerType, native_enum=False, validate_strings=True)
    )
    typical_offset_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    disbursement_note_md: Mapped[str] = mapped_column(Text, default="")

    track: Mapped[SchemeTrack] = relationship(back_populates="milestone_templates")
    document_requirements: Mapped[list["DocumentRequirement"]] = relationship(
        back_populates="milestone_template",
        cascade="all, delete-orphan",
        order_by="DocumentRequirement.id",
    )


class DocumentRequirement(Base, TimestampMixin, CitationMixin):
    """A document the scheme requires in support of a milestone."""

    __tablename__ = "document_requirement"

    id: Mapped[int] = mapped_column(primary_key=True)
    milestone_template_id: Mapped[int] = mapped_column(
        ForeignKey("milestone_template.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(300))
    description_md: Mapped[str] = mapped_column(Text, default="")
    issuing_authority: Mapped[str] = mapped_column(String(300), default="")
    format_note: Mapped[str] = mapped_column(Text, default="")

    milestone_template: Mapped[MilestoneTemplate] = relationship(
        back_populates="document_requirements"
    )


class Faq(Base, TimestampMixin, CitationMixin):
    """A question and its sourced answer. scheme_id is null for cross-scheme questions."""

    __tablename__ = "faq"

    id: Mapped[int] = mapped_column(primary_key=True)
    scheme_id: Mapped[int | None] = mapped_column(
        ForeignKey("scheme.id", ondelete="CASCADE"), nullable=True, index=True
    )
    question: Mapped[str] = mapped_column(Text)
    answer_md: Mapped[str] = mapped_column(Text)

    scheme: Mapped[Scheme | None] = relationship(back_populates="faqs")


class SourceDocument(Base, TimestampMixin):
    """An ingested primary document. full_text is chunked and indexed for search in Phase 4."""

    __tablename__ = "source_document"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500))
    url: Mapped[str] = mapped_column(String(1000))
    publisher: Mapped[str] = mapped_column(String(300), default="")
    published_on: Mapped[date | None] = mapped_column(nullable=True)
    retrieved_on: Mapped[date]
    local_path: Mapped[str] = mapped_column(String(1000), default="")
    full_text: Mapped[str] = mapped_column(Text, default="")
