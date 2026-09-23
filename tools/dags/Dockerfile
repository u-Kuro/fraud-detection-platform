FROM python:3.12.13-slim AS test-base

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_PREFERENCE=only-system
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /usr/local/bin/uv

COPY tools/dags/pyproject.toml  ./pyproject.toml
COPY uv.lock                    ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

COPY dags               ./dags
COPY tests/dags         ./tests/dags

COPY tests/__init__.py  ./tests/__init__.py

FROM test-base AS test-dev

CMD ["uv", "run", "pytest", "tests", "--verbose"]

FROM test-base AS test

RUN uv run pytest tests --quiet