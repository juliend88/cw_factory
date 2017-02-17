#!/bin/bash -x

export REPO_DIR=sources



#check factory_network
heat stack-create -f ${REPO_DIR}/v2/heat/template-network.yaml factory

while true
  do
   heat stack-list | grep factory_network  | cut -d "|" -f4 | grep "CREATE_COMPLETE"
   if  [ $? -eq 0 ]
      then
        export NET_ID=$(heat output-show factory Network_id | sed -e 's/^"//' -e 's/"$//')
        export SG_ID=$(heat output-show factory Security_group | sed -e 's/^"//'  -e 's/"$//')
        break
      else
        echo "Wait for factory_network stack will be up"
    fi
 done


DATE=$(date +%Y-%m-%d:%H:%M:%S)


export IMG_TMP_ID=$(cat outputs-glance/id.txt)

export IMG_NAME=${OS_NAME}-${OS_VERSION}-${DATE}

export PROVISIONNER_FILE=${REPO_DIR}/v2/packer/provision.sh

export CLOUD_CONFIG_FILE=${REPO_DIR}/v2/packer/cloud-config/$(echo ${OS_NAME}|tr '[A-Z]' '[a-z]')-${OS_VERSION}.yaml


packer build ${REPO_DIR}/v2/packer/packer_os.json


glance image-delete ${IMG_TMP_ID}


mkdir -p result


openstack image list | grep ${IMG_NAME} | awk {'print $2'} > result/id.txt


cat result/id.txt


ls result/*

