#!/bin/bash
DOCKER_USER=skirpichenko
docker run -v $(pwd):/opt/kserve-demo -ePORT=8081 -p8081:8081 ${DOCKER_USER}/kserve-base:latest

# run inference
# curl localhost:8081/v1/models/tg-gcn-kserve-demo:predict -d @./input.json