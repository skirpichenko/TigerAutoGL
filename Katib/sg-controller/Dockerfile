FROM nvidia/cuda:11.3.1-base-ubuntu20.04

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
    wget \
    pip \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /opt
# Set up the Conda environment
ENV CONDA_AUTO_UPDATE_CONDA=false \
    PATH=/opt/miniconda/bin:$PATH
COPY environment.yml /opt/environment.yml
RUN curl -sLo /opt/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-py39_4.11.0-Linux-x86_64.sh \
 && chmod +x /opt/miniconda.sh \
 && /opt/miniconda.sh -b -p /opt/miniconda \
 && rm /opt/miniconda.sh \
 && conda env update -n base -f /opt/environment.yml \
 && rm /opt/environment.yml \
 && conda clean -ya

 RUN pip install --no-index torch-scatter -f https://data.pyg.org/whl/torch-1.10.0+cu113.html \
 && pip install --no-index torch-sparse -f https://data.pyg.org/whl/torch-1.10.0+cu113.html \
 && pip install --no-index torch-cluster -f https://data.pyg.org/whl/torch-1.10.0+cu113.html \
 && pip install --no-index torch-spline-conv -f https://data.pyg.org/whl/torch-1.10.0+cu113.html \
 && pip install torch-geometric \
 && pip cache purge

ENV GRPC_HEALTH_PROBE_VERSION v0.4.6

RUN git clone https://github.com/skirpichenko/TigerAutoGL.git
RUN pip install nni 
RUN cd ./TigerAutoGL/AutoGL && python setup.py install
# dev time  only
RUN pip install -e /opt/TigerAutoGL/AutoGL

RUN if [ "$(uname -m)" = "ppc64le" ] || [ "$(uname -m)" = "aarch64" ]; then \
    apt-get -y update && \
    apt-get -y install gfortran libopenblas-dev liblapack-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*; \
    fi

RUN if [ "$(uname -m)" = "ppc64le" ]; then \
    wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-ppc64le; \
    elif [ "$(uname -m)" = "aarch64" ]; then \
    wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-arm64; \
    else \
    wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-amd64; \
    fi && \
    chmod +x /bin/grpc_health_probe

ENV TARGET_DIR /opt/TigerAutoGL/Katib/sg-controller
WORKDIR ${TARGET_DIR}
RUN chgrp -R 0 ${TARGET_DIR} \
  && chmod -R g+rwX ${TARGET_DIR} \
  && chmod +X ${TARGET_DIR}/run.sh

COPY requirements.txt ${TARGET_DIR}/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir google-cloud-storage
ENV PYTHONPATH /opt/TigerAutoGL:${TARGET_DIR}:${TARGET_DIR}/pkg/apis/manager/v1beta1/python:${TARGET_DIR}/pkg/apis/manager/health/python
RUN git config --global --add safe.directory /opt/TigerAutoGL
ENTRYPOINT  ./run.sh
