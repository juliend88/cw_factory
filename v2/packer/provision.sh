#!/bin/bash -x


echo ${OS_NAME}

echo ${OS_VERSION}


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

   if [ "$(echo ${VER})" == "6" ]
     then
        sudo chkconfig haveged on
     else
        sudo systemctl enable haveged
   fi
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
