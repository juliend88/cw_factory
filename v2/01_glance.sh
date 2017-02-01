#!/usr/bin/env bash

echo $IMG_URL
wget $IMG_URL

FILE=$(echo "${IMG_URL##*/}")

openstack image create toto --disk-format qcow2 --container-format bare --file $FILE



TMP_IMG_ID="$(openstack image list --private | grep toto | tr "|" " " | tr -s " " | cut -d " " -f2)"

echo $TMP_IMG_ID