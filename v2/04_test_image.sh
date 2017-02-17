#!/bin/bash -x



heat output-show factory private_key >${HOME}/key.pem

cat ${HOME}/key.pem

chmod 600 ${HOME}/key.pem

#export NOSE_IMAGE_ID=$(cat outputs-for-test/id.txt)

export NOSE_IMAGE_ID=6622878a-c762-4a88-b594-c30f255dcc06

export NOSE_FLAVOR=16


export NOSE_KEYPAIR=factory_keypair

export NOSE_NET_ID=$(heat output-show factory Network_id | sed -e 's/^"//' -e 's/"$//')

export NOSE_PORT_ID=$(heat output-show factory Port | sed -e 's/^"//' -e 's/"$//')

export NOSE_SG_ID=$(heat output-show factory Security_group | sed -e 's/^"//'  -e 's/"$//')

export NOSE_VOLUME_ID=$(heat output-show factory Volume | sed -e 's/^"//'  -e 's/"$//')


#cd sources/v2/pytesting_os

cd pytesting_os


nosetests -sv


rm -rf ${HOME}/key.pem

heat stack-delete factory -y