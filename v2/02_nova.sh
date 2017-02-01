#!/usr/bin/env bash

openstack server create   --flavor s1.cw.small-1 --image "0cd4d722-b54c-4b90-b430-f82c9ede0d01" --key-name alikey  --security-group start-sg-start --nic net-id=7359a091-59a7-4e29-a068-ed2a64d8c068 --file /etc/cloud/cloud.cfg=cloud-init ayoung-test1
