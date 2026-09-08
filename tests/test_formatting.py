"""The shared date and currency helpers are the only formatters in the app, so pin them."""

from datetime import date, datetime
from decimal import Decimal

from app.services.formatting import (
    format_date,
    format_datetime,
    format_inr,
    format_inr_words,
    indian_group,
)


def test_dates_read_dd_mon_yyyy() -> None:
    assert format_date(date(2025, 8, 4)) == "04 Aug 2025"
    assert format_date(datetime(2025, 12, 31, 9, 5)) == "31 Dec 2025"
    assert format_date(None) == "—"


def test_datetime_appends_a_24h_clock() -> None:
    assert format_datetime(datetime(2025, 8, 4, 16, 5)) == "04 Aug 2025, 16:05"


def test_indian_digit_grouping() -> None:
    assert indian_group(Decimal(0)) == "0"
    assert indian_group(Decimal(999)) == "999"
    assert indian_group(Decimal(1000)) == "1,000"
    assert indian_group(Decimal(100000)) == "1,00,000"
    assert indian_group(Decimal(12345678)) == "1,23,45,678"
    assert indian_group(Decimal(-12345678)) == "-1,23,45,678"


def test_rupee_formatting() -> None:
    assert format_inr(12345678) == "₹1,23,45,678"
    assert format_inr(None) == "—"
    assert format_inr("not a number") == "—"


def test_rupee_words_pick_the_right_scale() -> None:
    assert format_inr_words(45000) == "₹45,000"
    assert format_inr_words(450000) == "₹4.50 lakh"
    assert format_inr_words(12345678) == "₹1.23 crore"
