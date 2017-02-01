#!/usr/bin/env bash

TMP_IMG_ID="$(openstack image list --private | grep toto | tr "|" " " | tr -s " " | cut -d " " -f2)"

echo $TMP_IMG_ID
openstack server create --flavor s1.cw.small-1 --image $TMP_IMG_ID --key-name alikey --security-group start-sg-start --nic net-id=7359a091-59a7-4e29-a068-ed2a64d8c068 --user-data cloud-init.yml ayoung-test1

openstack image delete $TMP_IMG_ID

#openstack server create  --flavor s1.cw.small-1 --image "6622878a-c762-4a88-b594-c30f255dcc06" --key-name jukey  --security-group default --nic net-id=32b1f969-3eed-48ff-a106-751ee10dc60b --file /etc/cloud/cloud.cfg=cloud-init.yml youwin
