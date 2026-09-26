FROM python:3.12.13-slim

RUN apt-get update \
    && apt-get install --no-install-recommends --yes \
        docker-cli=26.1.5+dfsg1-9+deb13u1 \
        docker-buildx=0.13.1+ds1-3 \
        bash=5.2.37-2+b10 \
    && rm --recursive --force /var/lib/apt/lists/*

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