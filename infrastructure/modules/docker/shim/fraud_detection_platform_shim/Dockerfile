FROM python:3.12.13-slim AS base

RUN apt-get update \
    && apt-get install --no-install-recommends --yes \
        docker-cli=26.1.5+dfsg1-9+deb13u1 \
        docker-buildx=0.13.1+ds1-3 \
        bash=5.2.37-2+b10 \
    && rm --recursive --force /var/lib/apt/lists/*

ENV PYTHON_DIRECTORY=/app/infrastructure/modules/shim/fraud_detection_platform_shim
ENV SCRIPT_DIRECTORY=$PYTHON_DIRECTORY/scripts

WORKDIR $PYTHON_DIRECTORY

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_PREFERENCE=only-system
ENV UV_PROJECT_ENVIRONMENT=$PYTHON_DIRECTORY/.venv

ENV PATH=$PYTHON_DIRECTORY/.venv/bin:$PATH

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /usr/local/bin/uv

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=infrastructure/modules/shim/fraud_detection_platform_shim/pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=infrastructure/modules/shim/fraud_detection_platform_shim/uv.lock,target=uv.lock \
    uv sync --package fraud_detection_platform_shim --locked

WORKDIR /app

EXPOSE 16138

CMD ["python", "-m", "uvicorn", "fraud_detection_platform_shim.main:app", "--host", "0.0.0.0", "--port", "16138"]