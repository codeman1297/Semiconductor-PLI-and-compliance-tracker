# India Semiconductor Project Tracker

A source-backed public intelligence database for semiconductor fabs, OSAT/ATMP, packaging, testing, and related major projects in India. The MVP prioritizes evidence, reviewability, and change history over indiscriminate scraping.

## Architecture

- **Frontend:** Next.js 15 + TypeScript, server-rendered public views and a minimal admin data-entry workflow.
- **Backend:** FastAPI + Pydantic + SQLAlchemy, documented interactively at `/docs`.
- **Database:** PostgreSQL in Docker (SQLite is supported for local tests).
- **Evidence:** A project needs a source to be created; sources, milestones, raw intake records, and material history are separate relational records.

## Quick start

```bash
cp .env.example .env
export ADMIN_API_KEY='use-a-long-random-secret'
docker compose up --build
# Separate terminal, after backend is healthy:
docker compose exec backend python /app/scripts/seed_data.py
```

Open [http://localhost:3000](http://localhost:3000), API docs at [http://localhost:8000/docs](http://localhost:8000/docs). The tracked seed set uses an official PIB Cabinet approval release as its evidence record; it is deliberately small until each additional record is individually reviewed.

## Local development

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=backend DATABASE_URL=sqlite:///./tracker.db alembic -c backend/alembic.ini upgrade head
PYTHONPATH=backend python scripts/seed_data.py
PYTHONPATH=backend uvicorn app.main:app --reload
cd frontend && npm install && npm run dev
```

## Test and quality commands

```bash
cd backend && pytest -q && ruff check app tests
cd frontend && npm run build
```

## Migrations

```bash
cd backend
PYTHONPATH=. alembic revision --autogenerate -m "describe change"
PYTHONPATH=. alembic upgrade head
PYTHONPATH=. alembic downgrade -1
```

Do not modify a production database manually.

## Admin workflow

1. Open `/admin`, provide `ADMIN_API_KEY`, and create a draft with supporting evidence.
2. Add/verify sources and project details through the protected `/api/admin` endpoints.
3. Set `publication_status` to `PUBLISHED` only after review. Material updates automatically create `project_history` records.

## Ingestion

`backend/app/ingestion` defines small interfaces for validated manual/RSS candidates, normalization, content hashes, and raw source storage. Fetching feeds is intentionally not enabled by default: sources must be reviewed for terms, robots policy, and reliability before collection.

## Deployment

Deploy the frontend and backend containers separately with managed PostgreSQL, set strong `ADMIN_API_KEY`, restrict `CORS_ORIGINS` to the public frontend, apply Alembic migrations as a release step, then run the seed/admin workflow. Docker Compose is suitable for local development; production should use managed secrets, backups, TLS, and database monitoring.

## Roadmap

P0 delivers evidence-first records, search, filtering, detail pages, dashboard, change history, protected admin writes, tests and CI. RSS intake, newsletter signup, automated extraction proposals, alerts, map views, API keys, payments, and supplier intelligence are intentionally deferred.

See [docs/methodology.md](docs/methodology.md), [docs/architecture.md](docs/architecture.md), and [docs/data-model.md](docs/data-model.md).
