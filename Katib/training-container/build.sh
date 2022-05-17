#!/usr/bin/env bash
cd ../../
ls
#cat ./Katib/training-container/Dockerfile
docker build -f ./Katib/training-container/Dockerfile .
#cd ./Katib/training-container