#!/usr/bin/env bash

TMP_IMG_NAME="$BASENAME-tmp-$BUILDMARK"
IMG=ubuntu-14.04-server-cloudimg-amd64-disk1.img

//OS_USERNAME=$(OS_USERNAME)
OS_USERNAME2=$OS_USERNAME
OS_PASSWORD2=$OS_PASSWORD

env
echo $maxence
echo OS_USERNAME2
openstack image create --disk-format qcow2 --container-format bare --file $IMG $TMP_IMG_NAME