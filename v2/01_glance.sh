#!/usr/bin/env bash

#USAGE : sh 01_glance.sh

wget $IMG_URL

FILE=$(echo "${IMG_URL##*/}")

DATE=`date +%Y-%m-%d:%H:%M:%S`

openstack image create $FILE-$DATE --disk-format qcow2 --container-format bare --file $FILE

mkdir -p result
openstack image list | grep $FILE-$DATE | awk {'print $2'} >> result/id.txt

ls result/*