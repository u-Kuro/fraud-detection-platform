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

RUN uv sync --frozen --only-group fraud_detection_api --only-group test --no-install-project

COPY services/fraud_detection_api ./fraud_detection_api
COPY services/services_shared ./services_shared

FROM test-base AS test-dev

CMD ["python", "-m", "pytest", "fraud_detection_api/tests", "services_shared/tests", "--verbose"]

FROM test-base AS test

RUN python -m pytest fraud_detection_api/tests services_shared/tests --quiet

FROM base AS runtime

RUN uv sync --frozen --only-group fraud_detection_api --no-install-project

COPY services/fraud_detection_api/src ./fraud_detection_api/src
COPY services/services_shared/src ./services_shared/src

COPY services/fraud_detection_api/__init__.py ./fraud_detection_api/__init__.py
COPY services/services_shared/__init__.py ./services_shared/__init__.py

RUN useradd --create-home app_user && chown --recursive app_user /app
USER app_user

EXPOSE 8080

CMD ["uvicorn", "fraud_detection_api.src.main:app", "--host", "0.0.0.0", "--port", "8080"]