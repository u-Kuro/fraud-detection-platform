FROM python:3.12.13-slim AS test-dev

WORKDIR /app

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.11.10 /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --only-group dags --only-group test --no-install-project

COPY dags ./dags
COPY tests/dags ./tests/dags

COPY tests/__init__.py ./tests/__init__.py

CMD ["python", "-m", "pytest", "tests/dags", "--verbose"]