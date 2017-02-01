#!/usr/bin/env bash

TMP_IMG_NAME="$BASENAME-tmp-$BUILDMARK"
IMG=ubuntu-14.04-server-cloudimg-amd64-disk1.img

openstack image create --disk-format qcow2 --container-format bare --file image-tmp-name toto