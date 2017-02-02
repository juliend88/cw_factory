#!/usr/bin/env bash

NOVA_ID=$(cat outputs-glance/id.txt)
echo $NOVA_ID


openstack stack create factory_network -t sources/v2/heat/template.network.yaml

openstack stack show factory_network

NET_ID=$(openstack stack output show -f value  factory_network Network_id | sed -n '3p')
SG_ID=$(openstack stack output show -f value  factory_network Network_id | sed -n '3p')


packer build -var "source_image=$NOVA_ID" -var 'image_name=test_packer_aaaa' -var "factory_network=$NET_ID" -var "factory_security_group_name=$SG_ID" sources/v2/packer/packer_ubuntu.json

openstack stack delete factory_network

