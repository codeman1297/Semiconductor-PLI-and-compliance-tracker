"""Public, unauthenticated pages."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.templating import render

router = APIRouter(tags=["public"])


@router.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    """Landing page."""
    return render(request, "public/home.html")
