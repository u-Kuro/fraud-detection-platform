FROM python:3.12.13-slim AS base

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_PREFERENCE=only-system
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /usr/local/bin/uv

COPY services/dags_images/pyproject.toml    ./pyproject.toml
COPY uv.lock                                ./

COPY services/dags_images/drift_check       ./drift_check
COPY services/shared                        ./shared

FROM base AS test-base

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --only-group test_drift_check

COPY tests/services/dags_images/drift_check     ./tests/services/dags_images/drift_check
COPY tests/services/shared                      ./tests/services/shared

COPY tests/__init__.py                          ./tests/__init__.py
COPY tests/services/__init__.py                 ./tests/services/__init__.py
COPY tests/services/dags_images/__init__.py     ./tests/services/dags_images/__init__.py

FROM test-base AS test-dev

CMD ["uv", "run", "pytest", "tests", "--verbose"]

FROM test-base AS test

RUN uv run pytest tests --quiet

FROM base AS runtime

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --only-group drift_check \

RUN rm --force /usr/local/bin/uv

RUN useradd --create-home app_user && chown --recursive app_user /app
USER app_user

CMD ["python", "-m", "drift_check.main"]