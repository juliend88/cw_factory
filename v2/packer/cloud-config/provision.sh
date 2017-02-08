#!/usr/bin/env bash


echo ${OS_NAME}

echo ${OS_VERSION}



### Clean
sudo mv /tmp/cloud-config.yaml /etc/cloud/cloud.cfg
sudo rm -rf /home/cloud/.ssh/*
sudo service rsyslog stop
sudo rm -rf /var/log/*,
sudo rm -rf /home/cloud/*