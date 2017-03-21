#!/bin/bash -x


IMG_ID=$(cat outputs-packer/id.txt)

PURGE=$(openstack image show -f value -c properties ${IMG_ID} | tr ", " "\n" | grep -v "^$" | cut -d"=" -f1 | grep -v -E "(cw_os|cw_origin|hw_rng_model)" | sed 's/^/--remove-property /g' | tr "\n" " ")

glance image-update ${PURGE} ${IMG_ID}

glance image-update ${IMG_ID} --property  cw_cat=open_source --property hw_mg_model=virtio --property cw_origin=Cloudwatt --property cw_os=${OS_NAME}-${OS_VERSION} --property cw_logo=

glance image-update ${IMG_ID} --property  schema=/v2/schemas/image --min-disk 20


mkdir -p result

echo ${IMG_ID} > result/id.txt

cat result/id.txt

ls result/*