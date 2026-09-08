"""Controlled vocabularies. Member names equal their values so the stored text is readable."""

from enum import StrEnum


class SchemeStatus(StrEnum):
    open = "open"
    closed = "closed"
    announced = "announced"
    superseded = "superseded"


class TriggerType(StrEnum):
    date = "date"
    event = "event"
    percentage_of_capex = "percentage_of_capex"
    production_start = "production_start"


class Confidence(StrEnum):
    verified_primary_source = "verified_primary_source"
    secondary_source = "secondary_source"
    needs_review = "needs_review"


class ApplicationStatus(StrEnum):
    preparing = "preparing"
    applied = "applied"
    approved = "approved"
    in_disbursement = "in_disbursement"
    closed = "closed"


class MilestoneStatus(StrEnum):
    not_started = "not_started"
    in_progress = "in_progress"
    submitted = "submitted"
    disbursed = "disbursed"
    blocked = "blocked"
    na = "na"


class DocumentStatus(StrEnum):
    missing = "missing"
    drafting = "drafting"
    ready = "ready"
    submitted = "submitted"
