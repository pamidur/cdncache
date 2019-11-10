FROM alpine:latest
LABEL author="Oleksandr Hulyi <ohulyi@outlook.com>"

ENV \
	GIT_SOURCES="https://github.com/uklans/cache-domains" \
	UPSTREAM_DNS="1.1.1.1 8.8.8.8 2606:4700:4700::1111 2001:4860:4860::8888" \
	EXTERNAL_IPS="" \
	TZ="Europe/Paris"

RUN	apk update && \
	apk add --no-cache git dnsmasq sniproxy nginx supervisor bind && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /var/cache/apk/* && \
	rm -rf /etc/sniproxy && \
	rm -rf /etc/nginx && \
	rm -rf /etc/bind && \
	rm -rf /etc/dnsmasq.conf && \
	mkdir /var/cache/bind && \
	mkdir -p /data/sources && \
	mkdir -p /data/logs && \
	mkdir -p /data/cache && \
	chmod -R 666 /data && \
	chown -R nobody:nobody /data

COPY overlay/ /

CMD ["/usr/bin/supervisord"]
