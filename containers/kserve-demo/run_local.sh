#!/bin/bash
docker run -ePORT=8081 -p8081:8081 ${DOCKER_USER}/kserve-base:latest