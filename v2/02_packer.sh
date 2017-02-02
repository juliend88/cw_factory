#!/usr/bin/env bash

ls -al *
ls outputs-glance/*

NOVA_ID=$(cat outputs-glance/id.txt)
echo $NOVA_ID


#packer build packer_${OS_VERSION}.json