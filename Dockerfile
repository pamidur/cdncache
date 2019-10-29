FROM alpine:latest
LABEL author="Oleksandr Hulyi <ohulyi@outlook.com>"

ENV GIT_SOURCES="https://github.com/uklans/cache-domains"
ENV UPSTREAM_DNS="1.1.1.1 8.8.8.8 2606:4700:4700::1111 2001:4860:4860::8888"

RUN	apk update && \
	apk add --no-cache git dnsmasq sniproxy nginx supervisor nano

RUN	rm -rf /var/lib/apt/lists/* && \
	rm -rf /var/cache/apk/* && \
	rm -rf /etc/sniproxy

COPY overlay/ /

CMD ["/usr/bin/supervisord"]
