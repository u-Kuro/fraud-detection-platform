FROM python:3.12.13-slim AS base

WORKDIR /app

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

COPY services/__init__.py ./services/__init__.py
COPY services/dags/__init__.py ./services/dags/__init__.py

FROM base AS test-base

RUN uv sync --frozen --only-group drift_check --only-group test --no-install-project

COPY services/dags/drift_check ./services/dags/drift_check
COPY services/shared ./services/shared

FROM test-base AS test-dev

CMD ["python", "-m", "pytest", "services/dags/drift_check/tests", "services/shared/tests", "--verbose"]

FROM test-base AS test

RUN python -m pytest services/dags/drift_check/tests services/shared/tests --quiet

FROM base AS runtime

RUN uv sync --frozen --only-group drift_check --no-install-project

COPY services/dags/drift_check/src ./services/dags/drift_check/src
COPY services/shared/src ./services/shared/src

COPY services/dags/drift_check/__init__.py ./services/dags/drift_check/__init__.py
COPY services/shared/__init__.py ./services/shared/__init__.py

RUN useradd --create-home app_user && chown --recursive app_user /app
USER app_user

CMD ["python", "-m", "services.dags.drift_check.src.main"]