FROM ubuntu:18.04

RUN apt-get update \
  && apt-get install -y python3-pip python3 \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

ENTRYPOINT [ "python3" ]