#!/usr/bin/env bash

NOVA_ID=$(cat outputs-glance/id.txt)
echo $NOVA_ID


packer build packer_${OS_VERSION}.json