#!/usr/bin/env bash

#OS base Inputs : IMG_URL , OS_NAME , OS_VERSION
#Bundle Inputs : BUNDLE_NAME,BASE_IMAGE_ID

wget ${IMG_URL}

FILE=$(echo "${IMG_URL##*/}")

DATE=$(date +%Y-%m-%d:%H:%M:%S)

glance image-create --name ${FILE}-${DATE} --disk-format qcow2 --container-format bare --file ${FILE}


export IMG_TMP_ID=$(openstack image list | grep ${FILE}-${DATE} | awk {'print $2'})


#check factory_network
heat stack-create -f ./v2/heat/template-network.yaml factory

while true
  do
   heat stack-list | grep factory | cut -d "|" -f4 | grep "CREATE_COMPLETE"
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


if [ ! -z ${OS_NAME} ] && [ ! -z ${OS_VERSION} ]
  then
  if [ -z $IMG_TMP_ID ]
    then
       echo "You tmp image is not existed in glance"
       exit 1
  else

  export IMG_NAME=${OS_NAME}-${OS_VERSION}-${DATE}
  export PROVISIONNER_FILE=./v2/packer/provision.sh
  export CLOUD_CONFIG_FILE=./v2/packer/cloud-config/$(echo ${OS_NAME}|tr '[A-Z]' '[a-z]')-${OS_VERSION}.yaml
  packer build ./v2/packer/packer_os.json
  glance image-delete ${IMG_TMP_ID}
  fi
elif [ ! -z ${BASE_IMAGE_ID} ] && [ ! -z ${BUNDLE_NAME} ]
   then
  export IMG_NAME=${BUNDLE_NAME}-${DATE}
  packer build ./v2/packer/packer_bundle.json

else

    echo "what do you do ? I think you don't specify the parameters!!!!"
    exit 1
fi


IMG_ID=$(openstack image list | grep ${IMG_NAME} | awk {'print $2'})

PURGE=$(openstack image show -f value -c properties ${IMG_ID} | tr ", " "\n" | grep -v "^$" | cut -d"=" -f1 | grep -v -E "(cw_os|cw_origin|hw_rng_model)" | sed 's/^/--remove-property /g' | tr "\n" " ")

glance image-update ${PURGE} ${IMG_ID}

glance image-update ${IMG_ID} --property  cw_cat=open_source --property hw_mg_model=virtio --property cw_origin=Cloudwatt --property cw_os=${OS_NAME}-${OS_VERSION}

glance image-update ${IMG_ID} --property  schema=/v2/schemas/image --min-disk 20


export NOSE_IMAGE_ID=${IMG_ID}

export NOSE_FLAVOR=16

export NOSE_NET_ID=$(heat output-show factory Network_id | sed -e 's/^"//' -e 's/"$//')

export NOSE_PORT_ID=$(heat output-show factory Port | sed -e 's/^"//' -e 's/"$//')

export NOSE_SG_ID=$(heat output-show factory Security_group | sed -e 's/^"//'  -e 's/"$//')

export NOSE_VOLUME_ID=$(heat output-show factory Volume | sed -e 's/^"//'  -e 's/"$//')

cd sources/v2/pytesting_os

nosetests -sv

heat stack-delete factory
