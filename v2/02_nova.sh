#!/usr/bin/env bash

openstack server create   --flavor s1.cw.small-1 --image "0cd4d722-b54c-4b90-b430-f82c9ede0d01" --key-name alikey  --security-group start-sg-start --nic net-id=7359a091-59a7-4e29-a068-ed2a64d8c068 --file /etc/cloud/cloud.cfg=cloud-init ayoung-test1






openstack server create   --flavor s1.cw.small-1 --image "6622878a-c762-4a88-b594-c30f255dcc06" --key-name jukey  --security-group b631b7d5-6212-4d2b-8c15-7a7d88d388f5 --nic net-id=505dae5a-7058-4fe3-a731-810e0a10357e --file /etc/cloud/cloud.cfg=cloud-init.yml youwin
