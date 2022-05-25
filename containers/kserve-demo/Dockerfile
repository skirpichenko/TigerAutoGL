FROM public.ecr.aws/j1r0q0g6/notebooks/notebook-servers/jupyter-pytorch:master-c7ed4a32

# install - requirements.txt
COPY --chown=jovyan:users requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt --quiet --no-cache-dir \
 && rm -f /tmp/requirements.txt

ENV TARGET_DIR /opt/training-container
WORKDIR ${TARGET_DIR}
COPY --chown=jovyan:users main.py ${TARGET_DIR}/main.py
ENTRYPOINT ["python3", "-m", "main"]