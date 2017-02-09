#!/bin/bash -x

TMP=$(echo ${OS_NAME}|tr '[A-Z]' '[a-z]')
VER=(${OS_VERSION//./ })


if [ "${TMP}" ==  "centos" ] || [ "${TMP}" == "fedora" ]
  then
    if [ "${TMP}" ==  "centos" ]
      then
       sudo rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-$(echo ${VER}).noarch.rpm
    fi

    sudo sed -i '/^Defaults\s*requiretty$/d'/etc/sudoers

    sudo sed -i 's|UUID=[A-Fa-f0-9-]*|/dev/vda1 |' /etc/fstab

    sudo sed -i 's|UUID=[A-Fa-f0-9-]*|/dev/vda1 |' /boot/grub/menu.lst

    sudo yum install -y haveged parted


fi



### Clean


if [ "${TMP}" == "debian" ]
then
  mv /tmp/cloud-config.yaml /etc/cloud/cloud.cfg
  cat /etc/cloud/cloud.cfg
else
  sudo mv /tmp/cloud-config.yaml /etc/cloud/cloud.cfg
fi

sudo rm -rf /home/cloud/.ssh/*
sudo service rsyslog stop
sudo rm -rf /var/log/*
sudo rm -rf /home/cloud/bash_history
sudo rm -rf /var/tmp/*