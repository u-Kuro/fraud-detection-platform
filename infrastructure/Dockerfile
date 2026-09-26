FROM docker/buildx-bin:0.36.1 AS buildx-bin
FROM docker:29.7.2-cli AS docker-cli
FROM alpine/helm:4.2.3 AS helm
FROM rancher/kubectl:v1.34.2 AS kubectl

FROM hashicorp/terraform:1.16.3

COPY --from=buildx-bin /buildx /usr/libexec/docker/cli-plugins/docker-buildx
COPY --from=docker-cli /usr/local/bin/docker /usr/local/bin/docker
COPY --from=helm /usr/bin/helm /usr/local/bin/helm
COPY --from=kubectl /bin/kubectl /usr/local/bin/kubectl

RUN apk add --no-cache aws-cli bash curl jq make sed

ENV DOCKER_CLI_EXPERIMENTAL=enabled

WORKDIR /app

ENV IS_INSIDE_FRAUD_DETECTION_PLATFORM_DOCKER=1

ENTRYPOINT ["make"]