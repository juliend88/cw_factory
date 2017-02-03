#!/usr/bin/env bash

IMG_ID=e8ac129a-39e3-4755-a4f9-87ac3779f33e

purg=$(openstack image show -f value -c properties $IMG_ID | tr ", " "\n" | grep -v "^$" | cut -d"=" -f1 | grep -v -E "(cw_os|cw_origin|hw_rng_model)" | sed 's/^/--remove-property /g' | tr "\n" " ")

glance image-update $purg $IMG_ID

glance image-update $IMG_ID --property  cw_cat=open_source --property cw_origin=Cloudwatt --property cw_os=Pfsense-2.3

glance image-update $IMG_ID --property  schema=/v2/schemas/image --min-disk 20


