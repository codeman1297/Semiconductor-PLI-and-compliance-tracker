"""Jinja2 environment: one place to register filters and globals used by every template."""

from datetime import date
from pathlib import Path
from typing import Any, cast

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.services.formatting import (
    format_date,
    format_datetime,
    format_inr,
    format_inr_words,
)

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
templates.env.filters["date"] = format_date
templates.env.filters["datetime"] = format_datetime
templates.env.filters["inr"] = format_inr
templates.env.filters["inr_words"] = format_inr_words

_settings = get_settings()
templates.env.globals["app_name"] = _settings.app_name
templates.env.globals["disclaimer"] = _settings.disclaimer


def render(
    request: Request, template_name: str, context: dict[str, Any] | None = None
) -> HTMLResponse:
    """Render a template with the request in context. Routers should use this, not templates."""
    ctx = dict(context or {})
    ctx.setdefault("now_year", date.today().year)
    return cast(HTMLResponse, templates.TemplateResponse(request, template_name, ctx))
