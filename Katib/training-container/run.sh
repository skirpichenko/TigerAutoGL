#!/usr/bin/env bash
echo "autogl-training-container is starting"
# replace newline wirh '#'
# export AUTOGL_SPEC=$(sed -z 's/\n/#/g;s/#$/\n/' autogl_spec.yaml)
# run training
python3 main.py "$@"