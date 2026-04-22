#!/bin/bash

docker rm -f nginx_container app_container db_container 2>/dev/null

docker network create my_network 2>/dev/null

docker run -d \
  --name db_container \
  --network my_network \
  -e POSTGRES_USER=task4-db \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=kompsetidb \
  postgres:15

docker run -d \
  --name app_container \
  --network my_network \
  --env-file .env \
  my_app

sleep 5

docker run -d \
  --name nginx_container \
  --network my_network \
  -p 80:80 \
  -v "$(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro" \
  -v "$(pwd)/ip.txt:/etc/nginx/conf.d/ip.txt:ro" \
  -v "$(pwd)/stop.html:/usr/share/nginx/html/stop.html:ro" \
  nginx:alpine