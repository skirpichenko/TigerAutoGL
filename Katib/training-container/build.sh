#!/usr/bin/env bash
cd ../../
docker build -t autogl-training-container  -f ./Katib/training-container/Dockerfile .
cd ./Katib/training-container