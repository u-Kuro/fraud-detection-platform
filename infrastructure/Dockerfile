FROM hashicorp/terraform:1.16.3

RUN apk add --no-cache \
    aws-cli=2.34.63-r0 \
    bash=5.3.9-r1 \
    jq=1.8.2-r0 \
    sed=4.9-r2 \
    docker-cli=29.5.3-r1 \
    docker-cli-buildx=0.34.1-r1 \
    helm=3.19.0-r8 \
    kubectl=1.36.1-r1 \
    make=4.4.1-r4

WORKDIR /app

ENV IS_INSIDE_FRAUD_DETECTION_PLATFORM_DOCKER=1

ENTRYPOINT ["/bin/bash", "-c"]