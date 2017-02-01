#!/bin/bash

BASENAME="ubuntu-14.04"
BUILDMARK="$(date +%Y-%m-%d-%H%M)"
IMG_NAME="$BASENAME-$BUILDMARK"
TMP_IMG_NAME="$BASENAME-tmp-$BUILDMARK"

IMG=ubuntu-14.04-server-cloudimg-amd64-disk1.img
IMG_URL=http://cloud-images.ubuntu.com/releases/14.04/release/$IMG
wget -q $IMG_URL
echo $IMG

#openstack server stop Test

#nova image-create --poll Test myTestSnapshot