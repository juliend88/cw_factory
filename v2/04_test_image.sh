#!/bin/sh -x


export NOSE_IMAGE_ID=$(cat outputs-for-test/id.txt)

export NOSE_FLAVOR=21


export NOSE_NET_ID=$(heat output-show factory Network_id | sed -e 's/^"//' -e 's/"$//')

export NOSE_PORT_ID=$(heat output-show factory Port | sed -e 's/^"//' -e 's/"$//')

export NOSE_SG_ID=$(heat output-show factory Security_group | sed -e 's/^"//'  -e 's/"$//')

export NOSE_VOLUME_ID=$(heat output-show factory Volume | sed -e 's/^"//'  -e 's/"$//')

cd sources/v2/pytesting_os

nosetests --nologcapture