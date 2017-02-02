#!/usr/bin/env bash

NOVA_ID=$(cat outputs-glance/id.txt)
echo $NOVA_ID

openstack network create
packer build -var "source_image=$NOVA_ID" -var 'image_name=test_packer_aaaa' -var 'factory_network=7359a091-59a7-4e29-a068-ed2a64d8c068' -var 'factory_security_group_name=start-sg-start' sources/v2/packer/packer_ubuntu.json

