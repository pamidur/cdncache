docker build -t cdncache:latest . && \
    docker run -d -p 53:53/udp -p 53:53/tcp -p 80:80/tcp -p 443:443/tcp -e EXTERNAL_IPS="127.0.0.1" --name cdncache cdncache:latest && \
    docker exec -it cdncache /bin/sh ; \
    docker stop cdncache && docker rm cdncache
    