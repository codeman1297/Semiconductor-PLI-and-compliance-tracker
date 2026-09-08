"""The single place that formats dates and rupee amounts for display.

UX rule: dates always read `DD Mon YYYY`; money always carries the rupee sign and
Indian digit grouping. Nothing else in the app may format these by hand.
"""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation

RUPEE = "₹"
LAKH = Decimal(100_000)
CRORE = Decimal(10_000_000)


def format_date(value: date | datetime | None, empty: str = "—") -> str:
    """`14 Aug 2025`. Returns `empty` for a missing date rather than an empty cell."""
    if value is None:
        return empty
    if isinstance(value, datetime):
        value = value.date()
    return f"{value.day:02d} {value:%b %Y}"


def format_datetime(value: datetime | None, empty: str = "—") -> str:
    """`14 Aug 2025, 16:05` — used by the activity log."""
    if value is None:
        return empty
    return f"{format_date(value)}, {value:%H:%M}"


def indian_group(amount: Decimal) -> str:
    """Group digits the Indian way: 12345678 -> 1,23,45,678."""
    quantised = amount.quantize(Decimal("1"))
    sign = "-" if quantised < 0 else ""
    digits = str(abs(quantised))
    if len(digits) <= 3:
        return f"{sign}{digits}"
    head, tail = digits[:-3], digits[-3:]
    parts: list[str] = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return f"{sign}{','.join(parts)},{tail}"


def _to_decimal(value: Decimal | float | int | str | None) -> Decimal | None:
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def format_inr(value: Decimal | float | int | str | None, empty: str = "—") -> str:
    """`₹1,23,45,678`. Rounded to whole rupees — this app never shows paise."""
    amount = _to_decimal(value)
    if amount is None:
        return empty
    return f"{RUPEE}{indian_group(amount)}"


def format_inr_words(value: Decimal | float | int | str | None, empty: str = "—") -> str:
    """`₹1.23 crore` / `₹4.50 lakh` — the scale a CFO reads at a glance."""
    amount = _to_decimal(value)
    if amount is None:
        return empty
    magnitude = abs(amount)
    if magnitude >= CRORE:
        return f"{RUPEE}{(amount / CRORE).quantize(Decimal('0.01'))} crore"
    if magnitude >= LAKH:
        return f"{RUPEE}{(amount / LAKH).quantize(Decimal('0.01'))} lakh"
    return format_inr(amount)
