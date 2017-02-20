#!/usr/bin/env bash
export OS_AUTH_URL=https://identity.fr1.cloudwatt.com/v2.0

# With the addition of Keystone we have standardized on the term **tenant**
# as the entity that owns the resources.
export OS_TENANT_ID=467b00f998064f1688feeca95bdc7a88
export OS_TENANT_NAME="0750180084_@_1455009201"
export OS_PROJECT_NAME="0750180084_@_1455009201"

# In addition to the owning entity (tenant), OpenStack stores the entity
# performing the action as the **user**.
export OS_USERNAME="mohamed.lachhab-ext+compute@cloudwatt.com"
export OS_PASSWORD="mohamedalilachhab123"

# If your configuration has multiple regions, we set that information here.
# OS_REGION_NAME is optional and only valid in certain environments.
export OS_REGION_NAME="fr1"
