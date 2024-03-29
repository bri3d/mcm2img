FROM alpine:3.15

RUN mkdir m 0750 -p /app/fonts && \
  apk add --update-cache python3 py3-pillow bash && \
  rm -rf /var/cache/apk/*

COPY ./mcm2img.py /app/mcm2img.py
COPY ./entrypoint.sh /app/entrypoint.sh

WORKDIR /app
VOLUME /app/fonts
ENTRYPOINT ["/app/entrypoint.sh"]
