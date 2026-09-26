FROM alpine:3.24.2

RUN apk add --no-cache curl

WORKDIR /app

RUN curl --silent --fail https://raw.githubusercontent.com/nektos/act/v0.2.89/install.sh | sh -s -- -b /usr/local/bin v0.2.89

ENTRYPOINT ["act"]