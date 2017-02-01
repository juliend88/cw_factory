#!/usr/bin/env bash

echo $IMG_URL
wget $IMG_URL

FILE=$(echo "${IMG_URL##*/}")

openstack image create toto --disk-format qcow2 --container-format bare --file $FILE

