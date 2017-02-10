#!/bin/bash -x


cat <<EOF > sources/v2/pytesting_os/clouds.yml
clouds:
  dc1:
    auth_url: ${OS_AUTH_URL}
    username: ${OS_USERNAME}
    password: ${OS_PASSWORD}
    project_name: ${OS_TENANT_NAME}
    region_name: ${OS_REGION_NAME}
    volume_api_version: 1
EOF


export NOSE_IMAGE_ID=$(cat outputs-for-test/id.txt)

export NOSE_FLAVOR=16

export NOSE_KEYPAIR=alikey

export FACTORY_NETWORK_ID=$(heat output-show factory_network Network_id | sed -e 's/^"//' -e 's/"$//')

cd sources/v2/pytesting_os
./run_test.sh


heat stack-delete factory_network -y