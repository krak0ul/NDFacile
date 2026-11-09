FROM python:3.12-slim-trixie

# RUN apt-get update

RUN useradd -ms /bin/bash ndf
USER ndf

WORKDIR /app
COPY . /app

ENV PATH=$PATH:/home/ndf/.local/bin

RUN pip install --editable .