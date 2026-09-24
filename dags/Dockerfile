FROM python:3.12.13-slim AS test-base

FROM python:3.12.13-slim AS base

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_PREFERENCE=only-system
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

ENV PATH=/app/.venv/bin:$PATH

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /usr/local/bin/uv

COPY dags/pyproject.toml dags/uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

COPY dags/dags          ./dags
COPY dags/tests         ./tests

FROM test-base AS test-dev

CMD ["uv", "run", "pytest", "tests", "--verbose"]

FROM test-base AS test

RUN uv run pytest tests --quiet