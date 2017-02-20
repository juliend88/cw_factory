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
import time, paramiko,os,re
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



    def boot_vm_with_userdata_and_port(self,userdata_path,keypair):
        nics = [{'port-id': env['NOSE_PORT_ID']}]

        server = self.nova_client.servers.create(name="test-server-" + self.current_time_ms(), image=env['NOSE_IMAGE_ID'],
                                                 flavor=env['NOSE_FLAVOR'],userdata=file(userdata_path),key_name=keypair.name, nics=nics)

        self.wait_server_is_up(server)
        return server


    def boot_vm(self,image_id=env['NOSE_IMAGE_ID'],flavor=env['NOSE_FLAVOR'],keypair='default'):
        nics = [{'net-id': env['NOSE_NET_ID']}]
        server = self.nova_client.servers.create(name="test-server-" + self.current_time_ms(), image=image_id,security_groups=[env['NOSE_SG_ID']],

                                                 flavor=flavor, key_name=keypair.name, nics=nics)
        self.wait_server_is_up(server)
        return server


    def get_server(self,server_id):
        return self.nova_client.servers.get(server_id)


    def destroy_server(self,server):
        self.nova_client.servers.delete(server)


    def current_time_ms(self):
        return str(int(round(time.time() * 1000)))


    def get_console_log(self,server):
        return self.nova_client.servers.get(server.id).get_console_output(length=600)


    def get_spice_console(self,server):
        return self.nova_client.servers.get(server.id).get_spice_console('spice-html5')


    def create_server_snapshot(self,server):
        snapshot = self.nova_client.servers.create_image(server,server.name+self.current_time_ms())
        return snapshot

    def get_image(self,image_id):
        return self.glance_client.images.get(image_id)



    def destroy_image(self,image_id):
        self.glance_client.images.delete(image_id)


    def initiate_ssh(self,floating_ip):
        counter = 0
        while counter < 50:
            counter += 1
            try:
                ssh_connection = paramiko.SSHClient()
                ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_connection.connect(
                    floating_ip.ip,
                    username='cloud',
                    key_filename= env['HOME']+'/.ssh/key.pem',
                    timeout=200)
                return ssh_connection
                print "SSH connection established to %s" % floating_ip.ip
            except paramiko.ssh_exception.NoValidConnectionsError:
                time.sleep(6)
                pass

        return None


    def create_floating_ip(self):
        floating_ip = self.nova_client.floating_ips.create('public')
        return floating_ip


    def associate_floating_ip_to_port(self,floating_ip):
        self.neutron_client.update_floatingip(floating_ip.id,{'floatingip': {'port_id': env['NOSE_PORT_ID'] }})


    def associate_floating_ip_to_server(self,floating_ip, server):
        self.nova_client.servers.get(server.id).add_floating_ip(floating_ip.ip)


    def delete_floating_ip(self,floating_ip):
        self.nova_client.floating_ips.delete(floating_ip.id)


    def rescue(self,server):
        self.wait_server_available(server)
        return self.nova_client.servers.get(server.id).rescue()


    def unrescue(self,server):
        self.wait_server_available(server)
        return self.nova_client.servers.get(server.id).unrescue()



    def attach_volume_to_server(self,server):
        self.nova_client.volumes.create_server_volume(server_id=server.id,volume_id=env['NOSE_VOLUME_ID'])

    def detach_volume_from_server(self,server):
        self.wait_server_is_up(server)
        self.nova_client.volumes.delete_server_volume(server.id,env['NOSE_VOLUME_ID'])


    def get_flavor_disk_size(self,flavor_id):
        return self.nova_client.flavors.get(flavor_id).disk


    def hard_reboot(self,server):
        self.nova_client.servers.get(server.id).reboot(reboot_type='HARD')
        print self.get_server(server.id).status
        time.sleep(20)


    def soft_reboot(self,server):
        self.nova_client.servers.get(server.id).reboot(reboot_type='SOFT')
        print self.get_server(server.id).status
        time.sleep(20)


    def wait_server_is_up(self,server):
        status =server.status
        while status != 'ACTIVE':
            time.sleep(20)
            print "wait for  server"
            print "the status of server is :" + self.get_server(server.id).status
            status = self.get_server(server.id).status
        print "server is up"



    def wait_for_cloud_init(self,server):
         while True:
           console_log = self.get_console_log(server)
           if re.search('^.*Cloud-init .* finished.*$', console_log, flags=re.MULTILINE):
             print("Cloudinit finished__________________________________________________________________")
             break
             time.sleep(6)
           else:
             print("Cloudinit end not detected**********************************************************")


    def wait_server_available(self,server):
        task_state = getattr(server,'OS-EXT-STS:task_state')
        while task_state is not None:
              time.sleep(20)
              print "the server is busy"
              task_state = getattr(self.get_server(server.id),'OS-EXT-STS:task_state')
        print "the server is available"

    def create_keypair(self):
        keypair= self.nova_client.keypairs.create(name="nose_keypair"+self.current_time_ms())
        private_key_filename = env['HOME']+'/.ssh/key.pem'
        fp = os.open(private_key_filename, os.O_WRONLY | os.O_CREAT, 0o600)
        with os.fdopen(fp, 'w') as f:
               f.write(keypair.private_key)
        return keypair


    def delete_keypair(self,keypair):
        self.nova_client.keypairs.delete(keypair.id)
        os.remove(env['HOME']+'/.ssh/key.pem')




