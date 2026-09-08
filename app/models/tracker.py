"""User data: one company per user, its applications, milestones and documents."""

from datetime import date, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, utcnow
from app.models.content import DocumentRequirement, MilestoneTemplate, Scheme, SchemeTrack
from app.models.enums import ApplicationStatus, DocumentStatus, MilestoneStatus


class User(Base):
    """Identified by email only; authentication is a magic link (Phase 5)."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    companies: Mapped[list["Company"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Company(Base, TimestampMixin):
    """The applicant entity. One per user in the MVP."""

    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(300))
    sector: Mapped[str] = mapped_column(String(200), default="")
    notes: Mapped[str] = mapped_column(Text, default="")

    user: Mapped[User] = relationship(back_populates="companies")
    applications: Mapped[list["Application"]] = relationship(
        back_populates="company", cascade="all, delete-orphan"
    )


class Application(Base, TimestampMixin):
    """One company's participation in one scheme track."""

    __tablename__ = "application"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), index=True
    )
    scheme_id: Mapped[int] = mapped_column(ForeignKey("scheme.id"), index=True)
    track_id: Mapped[int] = mapped_column(ForeignKey("scheme_track.id"), index=True)
    reference_no: Mapped[str] = mapped_column(String(200), default="")
    approval_date: Mapped[date | None] = mapped_column(nullable=True)
    approved_amount: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, native_enum=False, validate_strings=True),
        default=ApplicationStatus.preparing,
    )

    company: Mapped[Company] = relationship(back_populates="applications")
    scheme: Mapped[Scheme] = relationship()
    track: Mapped[SchemeTrack] = relationship()
    milestones: Mapped[list["MilestoneInstance"]] = relationship(
        back_populates="application",
        cascade="all, delete-orphan",
        order_by="MilestoneInstance.id",
    )
    activity: Mapped[list["ActivityLog"]] = relationship(
        back_populates="application", cascade="all, delete-orphan", order_by="ActivityLog.at"
    )


class MilestoneInstance(Base, TimestampMixin):
    """A milestone template copied onto an application, with the user's own dates and status."""

    __tablename__ = "milestone_instance"

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("application.id", ondelete="CASCADE"), index=True
    )
    milestone_template_id: Mapped[int | None] = mapped_column(
        ForeignKey("milestone_template.id"), nullable=True, index=True
    )
    custom_name: Mapped[str | None] = mapped_column(String(300), nullable=True)
    due_date: Mapped[date | None] = mapped_column(nullable=True)
    status: Mapped[MilestoneStatus] = mapped_column(
        Enum(MilestoneStatus, native_enum=False, validate_strings=True),
        default=MilestoneStatus.not_started,
    )
    owner_name: Mapped[str] = mapped_column(String(200), default="")
    notes_md: Mapped[str] = mapped_column(Text, default="")
    completed_on: Mapped[date | None] = mapped_column(nullable=True)

    application: Mapped[Application] = relationship(back_populates="milestones")
    template: Mapped[MilestoneTemplate | None] = relationship()
    documents: Mapped[list["DocumentInstance"]] = relationship(
        back_populates="milestone", cascade="all, delete-orphan", order_by="DocumentInstance.id"
    )

    @property
    def display_name(self) -> str:
        """The user's override wins; otherwise the template's name."""
        if self.custom_name:
            return self.custom_name
        return self.template.name if self.template else "Untitled milestone"


class DocumentInstance(Base, TimestampMixin):
    """A document the user must produce for a milestone instance."""

    __tablename__ = "document_instance"

    id: Mapped[int] = mapped_column(primary_key=True)
    milestone_instance_id: Mapped[int] = mapped_column(
        ForeignKey("milestone_instance.id", ondelete="CASCADE"), index=True
    )
    document_requirement_id: Mapped[int | None] = mapped_column(
        ForeignKey("document_requirement.id"), nullable=True, index=True
    )
    custom_name: Mapped[str | None] = mapped_column(String(300), nullable=True)
    status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus, native_enum=False, validate_strings=True),
        default=DocumentStatus.missing,
    )
    notes: Mapped[str] = mapped_column(Text, default="")

    milestone: Mapped[MilestoneInstance] = relationship(back_populates="documents")
    requirement: Mapped[DocumentRequirement | None] = relationship()

    @property
    def display_name(self) -> str:
        """The user's override wins; otherwise the requirement's name."""
        if self.custom_name:
            return self.custom_name
        return self.requirement.name if self.requirement else "Untitled document"


class ActivityLog(Base):
    """Append-only trail rendered in the exported status report."""

    __tablename__ = "activity_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("application.id", ondelete="CASCADE"), index=True
    )
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    actor_email: Mapped[str] = mapped_column(String(320))
    description: Mapped[str] = mapped_column(Text)

    application: Mapped[Application] = relationship(back_populates="activity")


class Lead(Base):
    """A request for paid advisory help, captured from /advisory."""

    __tablename__ = "lead"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), index=True)
    company: Mapped[str] = mapped_column(String(300), default="")
    message: Mapped[str] = mapped_column(Text, default="")
    source_page: Mapped[str] = mapped_column(String(300), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
