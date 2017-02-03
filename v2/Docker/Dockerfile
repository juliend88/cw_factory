FROM ubuntu:trusty
MAINTAINER CWT

RUN apt-get update && \
    apt-get install -y wget curl unzip python-keystoneclient python-swiftclient python-novaclient python-troveclient python-openstackclient \
    python-glanceclient python-cinderclient python-heatclient python-ceilometerclient python-neutronclient && \
    curl -L -o packer.zip https://releases.hashicorp.com/packer/0.12.2/packer_0.12.2_linux_amd64.zip && sudo unzip -d /bin packer.zip
