# India Semiconductor Incentive Compliance Tracker

A compliance and milestone tracker for India's semiconductor and electronics incentive
schemes (ISM, DLI, ECMS and comparable state schemes). It answers one question for a
founder, CFO or consultant holding an approval: **what do I submit, when, and to whom?**

Every scheme fact in this product carries a citation to the notification it came from.

> Informational only. Not legal, financial, or tax advice. Verify against the current
> official notification before acting.

## Status

**Phase 1 (skeleton) complete.** The app boots, serves a landing page and health checks,
and the full database schema is under Alembic. No scheme content is loaded yet — content
arrives in Phase 2 from hand-curated YAML in `data/schemes/`.

## Stack

Python 3.11 · FastAPI · Jinja2 server-rendered HTML · HTMX + Tailwind from CDN (no build
step) · SQLite via SQLAlchemy 2 + Alembic · pytest. One VM or container, no workers.

## Quick start

```bash
make install     # venv + dependencies, copies .env.example to .env
make migrate     # create/upgrade the SQLite database
make dev         # http://127.0.0.1:8000
```

Other targets: `make test`, `make lint`, `make fmt`, `make typecheck`, `make check`.

## Configuration

Copy `.env.example` to `.env` and edit. Nothing secret is committed. The database
defaults to `./data/tracker.db`.

## Layout

```
app/
  main.py          FastAPI entrypoint and router wiring
  config.py        settings from .env
  db.py            engine, session factory, DbSession dependency
  models/          SQLAlchemy tables (content + tracker)
  schemas/         Pydantic models for requests and YAML content
  routers/         one module per URL area
  services/        business logic; no ORM queries live in templates
  templates/       base.html + public/ + app/
data/schemes/      hand-curated scheme YAML (source of truth for content)
data/sources/      downloaded scheme PDFs (git-ignored)
scripts/           seed, validate, ingest
alembic/           migrations
tests/
```

## Endpoints so far

| Route      | Purpose                                  |
|------------|------------------------------------------|
| `/`        | Landing page                             |
| `/healthz` | Liveness — process is up                 |
| `/readyz`  | Readiness — process up and database answers |

## Adding a migration

```bash
make revision m="add whatever"
make migrate
```
