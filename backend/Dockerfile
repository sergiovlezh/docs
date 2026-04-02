# syntax=docker/dockerfile:1

FROM python:3.13-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /app

COPY pyproject.toml uv.lock ./

# --- production ---
FROM base AS prod

RUN uv sync --frozen --no-dev --no-install-project

COPY alembic.ini .
COPY alembic/ alembic/
COPY app/ app/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]

# --- development ---
FROM base AS dev

RUN uv sync --frozen --no-install-project

COPY entrypoint.dev.sh /entrypoint.dev.sh
RUN chmod +x /entrypoint.dev.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.dev.sh"]
