FROM nvidia/cuda:11.3.1-base-ubuntu20.04

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
 && rm -rf /var/lib/apt/lists/*

# Create a working directory
RUN mkdir /app
WORKDIR /app

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
 && chown -R user:user /app
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

# All users can use /home/user as their home directory
ENV HOME=/home/user
RUN chmod 777 /home/user

# Set up the Conda environment
ENV CONDA_AUTO_UPDATE_CONDA=false \
    PATH=/home/user/miniconda/bin:$PATH
COPY environment.yml /app/environment.yml
RUN curl -sLo ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh \
 && chmod +x ~/miniconda.sh \
 && ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh \
 && conda env update -n base -f /app/environment.yml \
 && rm /app/environment.yml \
 && conda clean -ya

RUN pip install --no-index torch-scatter -f https://data.pyg.org/whl/torch-1.10.0+cu113.html \
 && pip install --no-index torch-sparse -f https://data.pyg.org/whl/torch-1.10.0+cu113.html \
 && pip install --no-index torch-cluster -f https://data.pyg.org/whl/torch-1.10.0+cu113.html \
 && pip install --no-index torch-spline-conv -f https://data.pyg.org/whl/torch-1.10.0+cu113.html \
 && pip install torch-geometric

WORKDIR /home/user

# Set the default command to python3
# CMD ["python3"]

RUN pip install nni 
RUN git clone https://github.com/skirpichenko/TigerAutoGL.git
RUN cd ./TigerAutoGL/AutoGL && python setup.py install
# dev time only
RUN pip install -e /home/user/TigerAutoGL/AutoGL

ENV PYTHONPATH /home/user/TigerAutoGL:${PYTHONPATH}
WORKDIR /home/user/TigerAutoGL/containers/autogl
ENTRYPOINT  ./run.sh