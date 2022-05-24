#!/usr/bin/env bash
cd ../../
docker build -t skirpichenko/autogl-training-container:latest  -f ./Katib/training-container/Dockerfile .
cd ./Katib/training-container