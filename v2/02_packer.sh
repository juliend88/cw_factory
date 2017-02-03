#!/usr/bin/env bash

IMG_TMP_ID=$(cat outputs-glance/id.txt)


openstack stack create factory_network -t sources/v2/heat/template-network.yaml

openstack stack show factory_network

NET_ID=$(openstack stack output show -f value  factory_network Network_id | sed -n '3p')
SG_ID=$(openstack stack output show -f value  factory_network Network_id | sed -n '3p')
DATE=$(date +%Y-%m-%d:%H:%M:%S)
IMG_NAME=$OS_NAME-$OS_VERSION-$DATE


packer build -var "source_image=$IMG_TMP_ID" -var 'image_name=$IMG_NAME' -var "factory_network=$NET_ID" -var "factory_security_group_name=$SG_ID" sources/v2/packer/packer_apt.json

openstack stack delete factory_network

openstack image delete $NOVA_ID