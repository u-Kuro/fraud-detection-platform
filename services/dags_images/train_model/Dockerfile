# syntax=docker/dockerfile:1-labs
FROM scratch AS services
COPY services/ /

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

COPY --parents --from=services **/pyproject.toml uv.lock ./

COPY services/dags_images/train_model/train_model       ./dags_images/train_model/train_model
COPY services/shared/shared                             ./shared/shared

FROM base AS test-base

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --package train_model --locked

COPY services/dags_images/train_model/tests             ./dags_images/train_model/tests

FROM test-base AS test-dev

CMD ["uv", "run", "--directory", "dags_images/train_model", "pytest", "--verbose"]

FROM test-base AS test

RUN uv run --directory dags_images/train_model pytest --quiet

FROM base AS runtime

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --package train_model --no-dev --frozen --no-editable

RUN useradd --create-home app_user && chown --recursive app_user /app
USER app_user

CMD ["python", "-m", "train_model.main"]