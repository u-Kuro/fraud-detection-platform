FROM python:3.12.13-slim AS base

WORKDIR /app

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

COPY services/fraud_detection_api   ./fraud_detection_api
COPY services/shared                ./shared

FROM base AS test-base

RUN uv sync --frozen --only-group fraud_detection_api --only-group test --no-install-project

COPY tests/services/fraud_detection_api         ./tests/services/fraud_detection_api
COPY tests/services/shared                      ./tests/services/shared

COPY tests/__init__.py                          ./tests/__init__.py
COPY tests/services/__init__.py                 ./tests/services/__init__.py

FROM test-base AS test-dev

CMD ["python", "-m", "pytest", "tests", "--verbose"]

FROM test-base AS test

RUN python -m pytest tests --quiet

FROM base AS runtime

RUN uv sync --frozen --only-group fraud_detection_api --no-install-project

RUN useradd --create-home app_user && chown --recursive app_user /app
USER app_user

EXPOSE 8080

CMD ["uvicorn", "fraud_detection_api.main:app", "--host", "0.0.0.0", "--port", "8080"]