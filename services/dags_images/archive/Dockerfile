FROM python:3.12.13-slim AS base

WORKDIR /app

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

COPY services/dags_images/archive   ./archive
COPY services/shared                ./shared

FROM base AS test-base

RUN uv sync --frozen --only-group archive --only-group test --no-install-project

COPY tests/services/dags_images/archive         ./tests/services/dags_images/archive
COPY tests/services/shared                      ./tests/services/shared

COPY tests/__init__.py                          ./tests/__init__.py
COPY tests/services/__init__.py                 ./tests/services/__init__.py
COPY tests/services/dags_images/__init__.py     ./tests/services/dags_images/__init__.py

FROM test-base AS test-dev

CMD ["python", "-m", "pytest", "tests", "--verbose"]

FROM test-base AS test

RUN python -m pytest tests --quiet

FROM base AS runtime

RUN uv sync --frozen --only-group archive --no-install-project

RUN useradd --create-home app_user && chown --recursive app_user /app
USER app_user

CMD ["python", "-m", "archive.main"]