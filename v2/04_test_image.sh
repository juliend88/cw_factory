#!/bin/bash -x

python --version

pip3 --version

IMG_ID=$(cat outputs-for-test/id.txt)

echo ${IMG_ID}


ls -la sources/v2/pytesting_os


