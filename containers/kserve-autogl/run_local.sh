#!/bin/bash
DOCKER_USER=skirpichenko
docker run -v $(pwd):/opt/kserve-demo -ePORT=8080 -p8080:8080 ${DOCKER_USER}/kserve-autogl:latest

# run inference
# curl localhost:8080/v1/models/tg-gcn-kserve-autogl:predict -d @./input.json