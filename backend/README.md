# Docs — Backend

FastAPI backend for the Docs document manager.

## Stack

- **Python 3.13**
- **FastAPI** — API framework
- **SQLAlchemy** — ORM
- **Alembic** — Database migrations
- **SQLite** — Default database
- **uv** — Package and environment manager

## Project structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app factory
│   ├── database.py      # Engine, session, Base
│   ├── routers/         # HTTP layer — one file per resource
│   ├── services/        # Business logic
│   ├── models/          # SQLAlchemy ORM models
│   └── schemas/         # Pydantic request/response schemas
├── alembic/             # Migration scripts
├── tests/               # Pytest test suite
├── pyproject.toml
└── Dockerfile
```
