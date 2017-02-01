#!/usr/bin/env bash

fly -t lite login -c http://84.39.32.178:8080

fly set-pipeline --target lite --config v2/v2.yml --pipeline v2 --load-vars-from ../credentials.yml
