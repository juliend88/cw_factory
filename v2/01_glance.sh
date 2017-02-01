#!/usr/bin/env bash

wget http://cloud-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-amd64-disk1.img
openstack image create toto --disk-format qcow2 --container-format bare --file ubuntu-14.04-server-cloudimg-amd64-disk1.img