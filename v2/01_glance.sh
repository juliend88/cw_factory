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

if [ "$1" == "ubuntu" ]
  then
    wget http://cloud-images.ubuntu.com/releases/${$2}/release/ubuntu-${$2}-server-cloudimg-amd64-disk1.img
fi

if [ "$1" == "debian" ]
  then
    wget http://cloud-images.ubuntu.com/releases/${$2}/release/ubuntu-${$2}-server-cloudimg-amd64-disk1.img
fi


if [ "$1" == "centos" ]
  then
    wget http://cloud.centos.org/$1/$2/images/$1-$2-x86_64-GenericCloud.qcow2
fi

openstack image create ${$1}-${$2}-${DATE} --disk-format qcow2 --container-format bare --file ubuntu-14.04-server-cloudimg-amd64-disk1.img