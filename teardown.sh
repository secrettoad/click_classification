#!/usr/bin/env bash

docker rm -f -v click_demo_postgres
docker rm -f click_demo_server
docker rm -f click_demo_ml
docker network rm myNetwork