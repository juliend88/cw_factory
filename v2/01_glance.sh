#!/usr/bin/env bash

DATE=`date +%Y-%m-%d:%H:%M:%S`

if [ -z "$1" ]
  then
    echo "L'OS n'est pas fourni"
fi

if [ -z "$2" ]
  then
    echo "La version n'est pas fourni"
fi

if [ -z "$3" ]
  then
    echo "URL de l'image"
fi

if [ "$1" == "ubuntu" ]
    then
        echo "Use Ubuntu"
        wget -O image.img $3
        openstack image create $1-$2-$DATE --disk-format qcow2 --container-format bare --file image.img
fi

if [ "$1" == "debian" ] || [ "$1" == "centos" ]
    then
        echo "Use Debian or CentOS"
        wget -O image.qcow2 $3
        openstack image create $1-$2-$DATE --disk-format qcow2 --container-format bare --file image.qcow2

fi
