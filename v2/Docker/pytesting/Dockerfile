# Dockerfile for building a development environment to work with the
# OpenStack Python SDK Shade to create cloud native apps.

FROM ubuntu:xenial
MAINTAINER CWT

# Update the repository sources list and install dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  libssl-dev \
  libffi-dev \
  python-dev \
  libxml2-dev \
  libxslt1-dev \
  python-pip \
  vim \
  git \
  wget

# Install Shade
ADD requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /root


