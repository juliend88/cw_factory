#!/usr/bin/env python
from openstackutils import OpenStackUtils
import time, shade, re, paramiko
from os import environ as env
import novaclient.exceptions as nova_exceptions



def get_cloud():
    global cloud
    if not cloud:
         cloud = OpenStackUtils()
    return cloud


#for i in  open.glance_client.images.list():
#      print i



def boot_vm_with_userdata_and_port(security_group, port, userdata_path):
    pass

    #return server




def boot_vm(security_group, image_id=env['NOSE_IMAGE_ID'], flavor=env['NOSE_FLAVOR']):
    nics = [{'net-id': net.id}]
    server = get_cloud().nova_client.servers.create(name="vm2", image=image_id,
                                      flavor=flavor, key_name=env['NOSE_KEYPAIR'], nics=nics)
    print(server)

    return server


def get_server(server_id):
    return get_cloud().nova_client.servers.get(server_id)


def destroy_server(server):
    get_cloud().nova_client.delete_server(server)


def current_time_ms():
    return str(int(round(time.time() * 1000)))


def create_port_with_sg(security_group):
    target_network = env['FACTORY_NETWORK_ID']
    #return get_cloud().create_port(target_network, security_groups=[security_group['id']])
    pass

def get_console_log(server):
    nova_server = get_cloud().nova_client.servers.get(server['id'])
    return nova_server.get_console_output(length=200)
    pass

def get_spice_console(shade_server):
    nova_server = get_cloud().nova_client.servers.get(shade_server['id'])
    return nova_server.get_spice_console('spice-html5')
    pass

def create_server_snapshot(shade_server):
     pass
    #return snapshot_image


def destroy_image(image_id):
    get_cloud().delete_image(image_id)


def initiate_ssh(floating_ip):
    counter = 0
    while counter < 30:
        counter += 1
        try:
            ssh_connection = paramiko.SSHClient()
            ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_connection.connect(
                floating_ip['floating_ip_address'],
                username='cloud',
                key_filename=env['HOME'] + '/.ssh/' + env['NOSE_KEYPAIR'] + '.pem',
                timeout=180
            )
            return ssh_connection
        except paramiko.ssh_exception.NoValidConnectionsError:
            time.sleep(6)
            pass

    return None


def get_image(image_id):
    return get_cloud().glance_client.images.delete(image_id)


def create_floating_ip():
    floating_ip = get_cloud().nova_client.floating_ips.create('public')
    print floating_ip
    return floating_ip


def associate_floating_ip_to_port(floating_ip, port):
    #neutron_client = get_cloud().neutron_client
    #neutron_client.update_floatingip(floating_ip['id'], {'floatingip': {'port_id': port['id']}})
    pass

def associate_floating_ip_to_server(floating_ip, server):
    get_cloud().nova_client.servers.get(server['id']).add_floating_ip(floating_ip['floating_ip_address'])


def create_security_group():
    #return get_cloud().get_security_group(new_security_group['id'])
    pass

def delete_security_group(security_group):
    #get_cloud().delete_security_group(security_group['id'])
    pass

def delete_floating_ip(floating_ip):
    get_cloud().nova_client.floating_ips.delete(floating_ip['id'])


def delete_port(port):
    #get_cloud().delete_port(port['id'])
    pass

def add_ssh_ingress_rule(security_group_id):
    #get_cloud().create_security_group_rule(security_group_id,
     #                                      port_range_min=22,
     #                                      port_range_max=22,
     #                                      protocol='TCP')
     pass

def create_volume():
    #created_volume = get_cloud().create_volume(5, True, 180)
    #return created_volume
    pass

def rescue(shade_server):
    #nova_client = get_cloud().nova_client
    #nova_client.servers.get(shade_server['id']).rescue()
    pass

def attach_volume_to_server(shade_server, shade_volume):
    #get_cloud().attach_volume(shade_server, shade_volume, '/dev/vdb', True, 180)
    #return get_cloud().get_volume(shade_volume['id'])
    pass

def detach_volume_from_server(shade_server, shade_volume):
    #get_cloud().detach_volume(shade_server, shade_volume, True, 180)
    pass

def get_flavor_disk_size(flavor_id):
    #return get_cloud().get_flavor(flavor_id)
    pass

def hard_reboot(shade_server):
    #nova_client = get_cloud().nova_client
    #nova_client.servers.get(shade_server['id']).reboot(reboot_type='HARD')
    #time.sleep(60)
    #wait_for_cloud_init(shade_server)
    pass

def soft_reboot(shade_server):
    #nova_client = get_cloud().nova_client
    #nova_client.servers.get(shade_server['id']).reboot(reboot_type='SOFT')
    #time.sleep(60)
    #wait_for_cloud_init(shade_server)
    pass
if __name__ == "__main__":
    open = OpenStackUtils()
    for i in  open.nova_client_client.servers.list():
        print i