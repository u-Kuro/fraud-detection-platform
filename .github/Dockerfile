FROM docker/buildx-bin:0.36.1 AS buildx-bin
FROM docker:29.7.2-cli AS docker-cli

FROM alpine:3.24.2

COPY --from=buildx-bin /buildx /usr/libexec/docker/cli-plugins/docker-buildx
COPY --from=docker-cli /usr/local/bin/docker /usr/local/bin/docker

RUN apk add --no-cache curl

WORKDIR /app

RUN curl --silent --fail https://raw.githubusercontent.com/nektos/act/v0.2.89/install.sh | sh -s -- -b /usr/local/bin v0.2.89

ENTRYPOINT ["act"]