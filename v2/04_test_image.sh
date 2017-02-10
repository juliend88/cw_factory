#!/bin/bash -x

python3 --version

pip3 --version

export NOSE_IMAGE_ID=$(cat outputs-for-test/id.txt)

export NOSE_FLAVOR=

export NOSE_KEYPAIR=



cd sources/v2/pytesting_os

ls

#nosetests -sv


