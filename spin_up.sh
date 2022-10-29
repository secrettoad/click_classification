#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
mkdir ${SCRIPT_DIR}/artifacts

docker build -t click_demo/ml ./ml
docker build -t click_demo/server ./server

docker network create myNetwork --subnet 172.99.42.1/16
docker run -e POSTGRES_HOST_AUTH_METHOD=trust -p 5432:5432 -d --name=click_demo_postgres postgres
sleep 5
python3 db_init.py
docker network connect --ip=172.99.42.2 myNetwork click_demo_postgres
docker run -v ${SCRIPT_DIR}/artifacts:/artifacts -t -d --network=myNetwork --name=click_demo_ml click_demo/ml
docker run -v ${SCRIPT_DIR}/artifacts:/artifacts -p 7999:7999 -d --network=myNetwork --name=click_demo_server click_demo/server
python3 -m pytest test
