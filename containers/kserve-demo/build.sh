#!/bin/bash

set -e

if [ -z "$1" ]; then
    version="latest"
else
    version=$1
fi

#echo "---- Collecting artifacts ----"
## Tutorials
#if [ -d "mlworkbench-docs" ]; then
#    cd mlworkbench-docs;
#    git pull
#    cd ..
#else
#    git clone https://github.com/TigerGraph-DevLabs/mlworkbench-docs.git
#fi


# Build the base Jupyter image
echo ---- Building image ---- 
docker build --rm -t kserve-base:${version} .

echo ---- Pushing to docker hub ----
# replace "skirpichenko" with "tigergraphml"
export DOCKER_USER=skirpichenko
docker tag kserve-base:${version} skirpichenko/kserve-base:${version}
docker push skirpichenko/kserve-base:${version}

#echo ---- Clean up ----
#rm -rf mlworkbench-docs