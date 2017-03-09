#!/bin/bash -x

TMP=$(echo ${OS_NAME}|tr '[A-Z]' '[a-z]')
VER=(${OS_VERSION//./ })


if [ "${TMP}" ==  "centos" ] || [ "${TMP}" == "fedora" ]
  then
    if [ "${TMP}" ==  "centos" ]
      then
       sudo yum install -y epel-release
       sudo yum install -y haveged parted curl unzip wget
      else
       sudo dnf install -y haveged parted curl unzip wget
    fi


    if [ "$(echo ${VER})" == "6" ]
      then
        sudo chkconfig haveged on
      else
        sudo systemctl enable haveged
    fi

    sudo sed -i '/^Defaults\s*requiretty$/d'/etc/sudoers

    sudo sed -i 's|UUID=[A-Fa-f0-9-]*|/dev/vda1 |' /etc/fstab

    sudo sed -i 's|UUID=[A-Fa-f0-9-]*|/dev/vda1 |' /boot/grub/menu.lst


else

    sudo apt-get update
    sudo apt-get install -y haveged curl bzip2 unzip


fi



### Clean

sudo mv /tmp/cloud-config.yaml /etc/cloud/cloud.cfg
sudo rm -rf /home/cloud/.ssh/*
sudo service rsyslog stop
sudo rm -rf /var/log/*
sudo rm -rf /home/cloud/bash_history
sudo rm -rf /var/tmp/*
sudo rm -rf /tmp/*