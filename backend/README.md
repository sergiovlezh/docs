# Docs — Backend

FastAPI backend for the Docs document manager.

## Stack

- **Python 3.13**
- **FastAPI** — API framework
- **SQLAlchemy** — ORM
- **Alembic** — Database migrations
- **SQLite** — Default database
- **uv** — Package and environment manager

## Code Quality

- **Ruff** — linter and formatter (replaces flake8, isort, and black)
- **pre-commit** — runs Ruff and validates commit messages before every commit

### Setup
```bash
uv sync
pre-commit install
pre-commit install --hook-type commit-msg
```

### Commit message format

This project uses [Conventional Commits](https://www.conventionalcommits.org/):
```
type: short description

# Examples
feat: add document upload endpoint
fix: handle missing file on download
chore: update ruff version
docs: add pre-commit setup instructions
refactor: extract file validation to service layer
test: add document creation tests
```

### Verify pre-commit is working
```bash
# Run against all files
pre-commit run --all-files

# Test commit message validation
git commit --allow-empty -m "chore: test conventional commit hook"
```

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
