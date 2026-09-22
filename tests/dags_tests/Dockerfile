FROM python:3.12.13-slim AS test-base

WORKDIR /app

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/dags
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --only-group dags --only-group test --no-install-project

COPY dags ./dags
COPY tests/dags_tests ./dags_tests

FROM test-base AS test-dev

CMD ["python", "-m", "pytest", "dags_tests", "--verbose"]

FROM test-base AS test

RUN python -m pytest dags_tests --quiet