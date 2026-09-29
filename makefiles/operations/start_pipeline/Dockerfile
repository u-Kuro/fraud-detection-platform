FROM alpine:3.24.2

RUN apk add --no-cache aws-cli bash make

WORKDIR /app

ENV IS_INSIDE_FRAUD_DETECTION_PLATFORM_DOCKER=true
ENV HOME=/tmp

ENTRYPOINT ["make"]