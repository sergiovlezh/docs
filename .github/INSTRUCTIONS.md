# Project Instructions - Docs (Document Manager)

> Stack: FastAPI (uv) · React + Vite + TypeScript · SQLite · Docker · Devcontainers · Monorepo

---

## 1. Overview

This is a monorepo containing the backend and frontend of **Docs**, a digital document management app inspired by Paperless NGX. The goal is to be deployable locally with Docker Compose, with devcontainer support for development.

The architecture follows a classic client-server model: the backend exposes a REST API and the frontend consumes it.

---

## 2. Repository Structure

```
docs/
├── .devcontainer/
│   ├── devcontainer.json        # Devcontainer main config
│   └── Dockerfile               # Devcontainer image
├── .github/
│   └── INSTRUCTIONS.md
├── backend/
│   ├── app/
│   ├── pyproject.toml
│   ├── ...
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── ...
│   └── Dockerfile
├── docker-compose.yml
├── DOMAIN.md
└── README.md
```

---

## 3. Backend - FastAPI + uv

### 3.1 Dependency management with uv

`uv` is used as the package and virtual environment manager. Never use `pip` directly.

`pyproject.toml` is the single source of truth for all dependencies. Do not use `requirements.txt`.

### 3.2 Layered structure

The backend is organized into 4 well-defined layers. Each layer only knows the one immediately below it:

**Router → Service → Model → Database**

| Layer | Responsibility |
|---|---|
| `routers/` | Handle HTTP requests, validate with Pydantic, delegate to service |
| `services/` | Business logic, orchestrate operations |
| `models/` | Table definitions using SQLAlchemy ORM |
| `schemas/` | Pydantic schemas for API input/output |

A router **never** accesses the database directly. That is the service's responsibility.

### 3.3 Python code conventions

- Use type hints in all functions.
- Request and response schemas must be separate (e.g. `DocumentCreate` vs `DocumentResponse`).
- IDs are always included in response schemas.

### 3.4 Database - SQLAlchemy + Alembic

SQLAlchemy is used with async sessions. SQLite is used in development; the connection URL is configured via environment variable to make future migration to PostgreSQL straightforward.

All migrations are managed with **Alembic**. Never use `Base.metadata.create_all()` outside of tests.

### 3.5 Authentication (MVP)

For the MVP, basic authentication is implemented via a simple username and password. The goal is to associate documents to a `user_id` from day one so that the ownership model works correctly without a full auth system.

- **Do not implement a custom JWT in this phase.** The user abstraction is what matters.

---

## 4. Frontend - React + Vite + TypeScript

### 4.1 Conventions

- All new code in strict TypeScript. No `any` unless justified with a comment.
- Components as functions, never classes.
- Types reflecting API responses live in `src/types/`, kept manually in sync with Pydantic schemas.
- Prefer composition over inheritance.

### 4.2 API communication

All communication with the backend is centralized in `src/api/`. Each file groups calls for one resource.

Do not mix fetch logic inside components. Use custom hooks in `src/hooks/` to encapsulate state and API calls.

### 4.3 Pages and components structure

- `pages/` contains route-level components (one file per page).
- `components/` contains reusable components, organized into subfolders as they grow.
- Pages orchestrate hooks and compose components - they do not contain business logic directly.

---

## 5. Code Quality

### 5.1 Backend

- Ruff acts as linter and formatter for all Python code. It replaces flake8, isort, and black.
- Backend tests live in `backend/tests/`.

### 5.2 Frontend

- Prettier acts as formatter for all TS/TSX code.
- Frontend tests must exist.

### 5.3 Pre-commit hooks

Pre-commit hooks run automatically before each commit. Every developer must install them once after cloning:
```bash
pre-commit install
pre-commit install --hook-type commit-msg
```

**Hooks configured:**
- `ruff check --fix`: lints and auto-fixes Python code
- `ruff format`: formats Python code
- `conventional-pre-commit`: enforces commit message format

**Commit message format:** `type: description`
Valid types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `ci`

Configuration lives in `.pre-commit-config.yaml` at the repo root.

### 5.4 CI Pipeline (GitHub Actions)

Runs automatically on every push and PR to `main` and `dev`.

**What it checks:**
- `ruff check` — lint
- `ruff format --check` — formatting
- `pytest` — test suite

Configuration lives in `.github/workflows/ci.yml`.

---

## 6. DX and Deployment

### 6.1 Devcontainer (development)

The devcontainer sets up a consistent development environment in VS Code. Configuration lives in `.devcontainer/` and uses its own `Dockerfile`.

### 6.2 Docker Compose (local production)

Used to run the full application locally, similar to Paperless NGX or Immich. The user should be able to spin up the app with a single command.

### 6.3 Dockerfiles

A Dockerfile must exist for both the backend and the frontend.

---

## 7. General Conventions

### Naming

| Element | Convention | Example |
|---|---|---|
| Python files | `snake_case` | `document_service.py` |
| Python classes | `PascalCase` | `DocumentService` |
| Python functions | `snake_case` | `get_document_by_id` |
| TS/TSX files | `camelCase` or `PascalCase` for components | `useDocuments.ts`, `DocumentCard.tsx` |
| TS variables/functions | `camelCase` | `getDocuments` |
| REST endpoints | `kebab-case`, plural nouns | `/api/documents`, `/api/document-files` |

### Error responses

Always use FastAPI's `HTTPException` with the appropriate HTTP status code and a clear message in English:

```python
raise HTTPException(status_code=404, detail="Document not found")
raise HTTPException(status_code=403, detail="Not authorized to access this document")
```

---

## 8. Out of Scope (for now)

- Full authentication with JWT or OAuth2.
- PostgreSQL (switching only requires changing `DATABASE_URL`).
- Full-text search.
- OCR.
- Async task workers (Celery/ARQ).