#!/usr/bin/env bash
# docker run --rm -i -t skirpichenko/autogl-training-container:latest

docker run --rm -i -t -e AUTOGL_SPEC="$(sed -z 's/\n/#/g;s/#$/\n/' autogl_spec.yaml)" -v $HOME/TigerAutoGL/Katib/training-container:/opt/training-container -v $HOME/TigerAutoGL/AutoGL:/opt/AutoGL skirpichenko/autogl-training-container:latest