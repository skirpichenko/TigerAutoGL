FROM pytorch/pytorch:1.0-cuda10.0-cudnn7-runtime

ADD . /opt/autogl
WORKDIR /opt/autogl

# Add folder for the logs.
RUN mkdir /katib

RUN chgrp -R 0 /opt/autogl \
  && chmod -R g+rwX /opt/autogl \
  && chgrp -R 0 /katib \
  && chmod -R g+rwX /katib

ENTRYPOINT ["python3", "/opt/autogl/main.py"]
