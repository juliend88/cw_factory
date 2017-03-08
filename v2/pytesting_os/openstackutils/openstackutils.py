#!/usr/bin/env python
#-*- coding: utf-8 -
import keystoneclient.v2_0.client as keystone
from keystoneauth1.identity import v2
from keystoneauth1 import session
import novaclient.client as nova
import cinderclient.client as cinder
from glanceclient.v1 import client as glance
import neutronclient.v2_0.client as neutron
import heatclient.client as heat
import time, paramiko,os,re,errno,random
from socket import error as socket_error
from os import environ as env

class OpenStackUtils():
    def __init__(self):
        auth = v2.Password(auth_url=env['OS_AUTH_URL'],
                           username=env['OS_USERNAME'],
                           password=env['OS_PASSWORD'],
                           tenant_id=env['OS_TENANT_ID'])
        sess = session.Session(auth=auth)
        self.keystone_client = keystone.Client(username=env['OS_USERNAME'],
                                               password=env['OS_PASSWORD'],
                                               tenant_id=env['OS_TENANT_ID'],
                                               auth_url=env['OS_AUTH_URL'],
                                               region_name=env['OS_REGION_NAME'])

        heat_url = self.keystone_client \
            .service_catalog.url_for(service_type='orchestration',
                                     endpoint_type='publicURL')

        self.nova_client = nova.Client('2.1', region_name=env['OS_REGION_NAME'], session=sess)
        self.cinder_client = cinder.Client('2', region_name=env['OS_REGION_NAME'], session=sess)
        self.glance_client = glance.Client('2', region_name=env['OS_REGION_NAME'], session=sess)
        self.neutron_client = neutron.Client(region_name=env['OS_REGION_NAME'], session=sess)
        self.heat_client = heat.Client('1', region_name=env['OS_REGION_NAME'], endpoint=heat_url, session=sess)


    def current_time_ms(self):
        return str(int(round(time.time() * 1000)))

    def boot_vm_with_userdata_and_port(self,userdata_path,keypair,port):
        nics = [{'port-id': port['port']['id'] }]
        server = self.nova_client.servers.create(name="test-server-" + self.current_time_ms(), image=env['NOSE_IMAGE_ID'],
                                                 flavor=env['NOSE_FLAVOR'],userdata=file(userdata_path),key_name=keypair.name, nics=nics)

        print 'Building, please wait...'
        # wait for server create to be complete
        self.wait_server_is_up(server)
        self.wait_for_cloud_init(server)
        return server

    def boot_vm(self,image_id=env['NOSE_IMAGE_ID'],flavor=env['NOSE_FLAVOR'],keypair='default'):
        nics = [{'net-id': env['NOSE_NET_ID']}]
        server = self.nova_client.servers.create(name="test-server-" + self.current_time_ms(), image=image_id,security_groups=[env['NOSE_SG_ID']],
                                                 flavor=flavor, key_name=keypair.name, nics=nics)
        print 'Building, please wait...'
        self.wait_server_is_up(server)
        self.wait_for_cloud_init(server)
        return server

    def wait_server_is_up(self,server):
        status = server.status
        while status != 'ACTIVE':
            status = self.get_server(server.id).status
        print "server is up"

    def wait_for_cloud_init(self,server):
        while True:
            console_log = self.get_console_log(server)
            if re.search('^.*Cloud-init .* finished.*$', console_log, flags=re.MULTILINE):
                print "Cloudinit finished"
                break
            else:
                time.sleep(10)

    def wait_server_available(self,server):
        task_state = getattr(server,'OS-EXT-STS:task_state')
        while task_state is not None:
            task_state = getattr(self.get_server(server.id),'OS-EXT-STS:task_state')
        print "the server is available"

    def get_server(self,server_id):
        return self.nova_client.servers.get(server_id)

    def destroy_server(self,server):
        self.nova_client.servers.delete(server)
        time.sleep(30)

    def get_console_log(self,server):
        return server.get_console_output(length=600)

    def get_spice_console(self,server):
        return server.get_spice_console('spice-html5')

######images######################
    def create_server_snapshot(self,server):
        return self.nova_client.servers.create_image(server,server.name+"-"+self.current_time_ms())

    def get_image(self,image_id):
        return self.glance_client.images.get(image_id)

    def destroy_image(self,image_id):
        self.glance_client.images.delete(image_id)

###ssh connexion
    def initiate_ssh(self,floating_ip,private_key_filename):
        ssh_connection = paramiko.SSHClient()
        ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        retries_left = 5
        while True:
             try:
                ssh_connection.connect(floating_ip.ip,username='cloud',key_filename=private_key_filename,timeout=180)
                break
             except socket_error as e:
                    if e.errno != errno.ECONNREFUSED or retries_left <= 1:
                       raise e
             time.sleep(10)  # wait 10 seconds and retry
             retries_left -= 1
        return ssh_connection

    def close_ssh_connextion(self,ssh_connection):
        if ssh_connection is not None:
            ssh_connection.close()
            ssh_connextion = None


###########floatingip###############
    def get_or_create_floating_ip(self,pool="public"):
        ip_list = self.nova_client.floating_ips.list()
        # Filtering out associated floating IPs
        ip_list = [ip for ip in ip_list if ip.instance_id is None]
        # Filtering floating IPs accord to a specific pool
        if pool is not None:
              ip_list = [ip for ip in ip_list if ip.pool == pool]
        if len(ip_list) > 0:
            # don't forget to import random
            return random.choice(ip_list)
        else:
            return self.nova_client.floating_ips.create(pool)

    def associate_floating_ip_to_server(self,floating_ip, server):
        server.add_floating_ip(floating_ip.ip)
        time.sleep(10)


    def delete_floating_ip(self,floating_ip):
        self.nova_client.floating_ips.delete(floating_ip.id)

##########action in servers#########
    def rescue(self,server):
        server.rescue()
        self.wait_server_available(server)


    def unrescue(self,server):
        server.unrescue()
        self.wait_server_available(server)


    def server_reboot(self,server,type):
        server.reboot(type)
        self.wait_server_is_up(server)


#######flavor##################

    def get_flavor_disk_size(self,flavor_id):
        return self.nova_client.flavors.get(flavor_id).disk

#######keypair#################

    def create_keypair(self):
        suffix =self.current_time_ms()
        keypair= self.nova_client.keypairs.create(name="nose_keypair-"+suffix)
        private_key_filename = env['HOME']+'/key-'+suffix+'.pem'
        fp = os.open(private_key_filename, os.O_WRONLY | os.O_CREAT, 0o600)
        with os.fdopen(fp, 'w') as f:
               f.write(keypair.private_key)
        return keypair , private_key_filename

    def delete_keypair(self,keypair,private_key_filename):
        self.nova_client.keypairs.delete(keypair.name)
        os.remove(private_key_filename)


##########port################
    def create_port_with_sg(self):
        body_value = {'port': {
                      'admin_state_up': True,
                      'security_groups': [env['NOSE_SG_ID']],
                      'name': 'port-test'+self.current_time_ms(),
                      'network_id': env['NOSE_NET_ID'],
                    }}
        port=self.neutron_client.create_port(body=body_value)
        time.sleep(20)
        return port


    def delete_port(self,port):
        self.neutron_client.delete_port(port['port']['id'])


#######volume##########
    def wait_volume_status(self,volume,status,type):
        while status != type:
            status = self.cinder_client.volumes.get(volume.id).status
            print status
        print "the status of volume is : "+ status

    def create_volume(self):
        volume=self.cinder_client.volumes.create(5, name="test-volume"+self.current_time_ms())
        print "the status of volume is:"+ volume.status
        self.wait_volume_status(volume,volume.status,'available')
        return volume

    def attach_volume_to_server(self,server,volume):
        self.nova_client.volumes.create_server_volume(server_id=server.id,volume_id=volume.id)
        self.wait_volume_status(volume,volume.status,'in-use')

    def detach_volume_from_server(self,server,volume):
        self.nova_client.volumes.delete_server_volume(server.id,volume.id)

    def delete_volume(self,volume):
        self.cinder_client.volumes.delete(volume.id)
