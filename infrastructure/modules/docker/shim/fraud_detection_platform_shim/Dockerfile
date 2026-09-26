FROM docker/buildx-bin:0.36.1 AS buildx-bin
FROM docker:29.7.2-cli AS docker-cli

FROM python:3.12.13-slim

COPY --from=buildx-bin /buildx /usr/libexec/docker/cli-plugins/docker-buildx
COPY --from=docker-cli /usr/local/bin/docker /usr/local/bin/docker

RUN apt-get update \
    && apt-get install --no-install-recommends --yes bash \
    && rm --recursive --force /var/lib/apt/lists/*

ENV DOCKER_CLI_EXPERIMENTAL=enabled

WORKDIR /opt/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_PREFERENCE=only-system
ENV UV_PROJECT_ENVIRONMENT=/opt/app/.venv

ENV PATH=/opt/app/.venv/bin:$PATH

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /usr/local/bin/uv

COPY infrastructure/modules/docker/shim/fraud_detection_platform_shim .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --package fraud_detection_platform_shim --locked

ENV SCRIPT_DIRECTORY=/opt/app/scripts

WORKDIR /app

EXPOSE 16138

CMD ["python", "-m", "uvicorn", "fraud_detection_platform_shim.main:app", "--host", "0.0.0.0", "--port", "16138"]