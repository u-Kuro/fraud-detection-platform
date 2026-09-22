FROM python:3.12.13-slim AS base

WORKDIR /app

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

FROM base AS test-base

RUN uv sync --frozen --only-group archive --only-group test --no-install-project

COPY services/dags_images/archive ./archive
COPY services/services_shared ./services_shared

FROM test-base AS test-dev

CMD ["python", "-m", "pytest", "archive/tests", "services_shared/tests", "--verbose"]

FROM test-base AS test

RUN python -m pytest archive/tests services_shared/tests --quiet

FROM base AS runtime

RUN uv sync --frozen --only-group archive --no-install-project

COPY services/dags_images/archive/src ./archive/src
COPY services/services_shared/src ./services_shared/src

COPY services/dags_images/archive/__init__.py ./archive/__init__.py
COPY services/services_shared/__init__.py ./services_shared/__init__.py

RUN useradd --create-home app_user && chown --recursive app_user /app
USER app_user

CMD ["python", "-m", "archive.src.main"]