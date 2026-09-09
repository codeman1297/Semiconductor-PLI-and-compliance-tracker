# Architecture

The browser uses a Next.js application that reads the FastAPI REST API. FastAPI owns validation, authorization for writes, change detection, OpenAPI documentation, and SQLAlchemy persistence to PostgreSQL. Raw source intake is separate from published project evidence, leaving a clean boundary for future RSS/AI proposals: candidates are stored and reviewed before they can change public records.
