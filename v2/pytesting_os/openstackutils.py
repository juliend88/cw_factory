import argparse
import logging
import os
import sys
import prettytable
import inspect
import threading
import time

import keystoneclient.v2_0.client as keystone
from keystoneauth1.identity import v2
from keystoneauth1 import session
import novaclient.client as nova
from novaclient import utils as nova_utils
import cinderclient.client as cinder
from glanceclient.v1 import client as glance
import neutronclient.v2_0.client as neutron
import heatclient.client as heat
import requests.packages.urllib3
import os


class OpenStackUtils():
    def __init__(self):
        auth = v2.Password(auth_url=os.environ['OS_AUTH_URL'],
                           username=os.environ['OS_USERNAME'],
                           password=os.environ['OS_PASSWORD'],
                           tenant_id=os.environ['OS_TENANT_ID'])
        sess = session.Session(auth=auth)
        self.keystone_client = keystone.Client(username=os.environ['OS_USERNAME'],
                                               password=os.environ['OS_PASSWORD'],
                                               tenant_id=os.environ['OS_TENANT_ID'],
                                               auth_url=os.environ['OS_AUTH_URL'],
                                               region_name=os.environ['OS_REGION_NAME'])

        heat_url = self.keystone_client \
            .service_catalog.url_for(service_type='orchestration',
                                     endpoint_type='publicURL')

        self.nova_client = nova.Client('2.1', region_name=os.environ['OS_REGION_NAME'], session=sess)
        self.cinder_client = cinder.Client('2', region_name=os.environ['OS_REGION_NAME'], session=sess)
        self.glance_client = glance.Client('2', region_name=os.environ['OS_REGION_NAME'], session=sess)
        self.neutron_client = neutron.Client(region_name=os.environ['OS_REGION_NAME'], session=sess)
        self.heat_client = heat.Client('1', region_name=os.environ['OS_REGION_NAME'], endpoint=heat_url, session=sess)

#if __name__ == "__main__":
#    open = OpenStackUtils()
#    for i in  open.glance_client.images.list():
#        print i