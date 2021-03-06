#!/usr/bin/env bash

PWD=$(pwd)
Directory=$(dirname $0)
echo "${Directory}"
echo "${PWD}"

fly -t lite login -c http://84.39.32.178:8080/

#fly set-pipeline --target lite --config ${PWD}/${Directory}/base-image-factory.yml --pipeline v15 --load-vars-from ~/credentials.yml

fly set-pipeline --target lite --config ${PWD}/${Directory}/os-image-factory.yml --pipeline v16 --load-vars-from ~/credentials.yml
