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
COPY ./Katib/training-container/environment.yml /opt/environment.yml
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

# install AutoGL
COPY ./AutoGL /opt/AutoGL
RUN pip install nni 
RUN cd /opt/AutoGL && python setup.py install

COPY ./Katib/training-container /opt/training-container

ENV TARGET_DIR /opt/training-container
WORKDIR ${TARGET_DIR}
RUN chgrp -R 0 ${TARGET_DIR} \
  && chmod -R g+rwX ${TARGET_DIR} \
  && chmod +X ${TARGET_DIR}/run.sh

ENTRYPOINT  ./run.sh