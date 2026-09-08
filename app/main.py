"""FastAPI application entrypoint."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routers import health, public

settings = get_settings()

STATIC_DIR = Path(__file__).resolve().parent / "static"


def create_app() -> FastAPI:
    """Build the app. Kept a factory so tests can construct isolated instances."""
    application = FastAPI(
        title=settings.app_name,
        docs_url="/api/docs" if settings.debug else None,
        redoc_url=None,
        openapi_url="/api/openapi.json" if settings.debug else None,
    )
    application.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    application.include_router(health.router)
    application.include_router(public.router)
    return application


app = create_app()
