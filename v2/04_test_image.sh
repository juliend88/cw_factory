#!/bin/bash -x



export NOSE_IMAGE_ID=$(cat outputs-for-test/id.txt)

export NOSE_FLAVOR=16

export NOSE_KEYPAIR=alikey

export NOSE_NET_ID=$(heat output-show factory_network Network_id | sed -e 's/^"//' -e 's/"$//')

cd sources/v2/pytesting_os

nosetests -sv

heat stack-delete factory_network -y