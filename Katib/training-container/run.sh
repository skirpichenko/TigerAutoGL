#!/usr/bin/env bash
echo "autogl-training-container is starting"
export AUTOGL_SPEC=$(cat autogl_spec.yaml)

python3 main.py "$@"