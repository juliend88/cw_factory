#!/usr/bin/env bash

TMP_IMG_NAME="$BASENAME-tmp-$BUILDMARK"
IMG=ubuntu-14.04-server-cloudimg-amd64-disk1.img

OS_USERNAME=$(OS_USERNAME)

env
echo $maxence
echo OS_USERNAME
openstack image create --disk-format qcow2 --container-format bare --file $IMG $TMP_IMG_NAME