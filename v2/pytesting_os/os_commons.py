#!/usr/bin/env python
from openstackutils import OpenStackUtils
import time, re, paramiko
from os import environ as env



def get_cloud():
    return OpenStackUtils()


def boot_vm_with_userdata_and_port(security_group, port, userdata_path):
    nics = [{'port-id': port.id}]
    server = get_cloud().nova_client.servers.create(name="test-server-" + current_time_ms(), image=env['NOSE_IMAGE_ID'],security_groups=[security_group['name']],
                                                    flavor=env['NOSE_FLAVOR'], key_name=env['NOSE_KEYPAIR'], userdata=file(userdata_path), nics=nics)

    return server

def boot_vm(security_group, image_id=env['NOSE_IMAGE_ID'], flavor=env['NOSE_FLAVOR']):
    nics = [{'net-id': env['NOSE_NET_ID']}]
    server = get_cloud().nova_client.servers.create(name="test-server-" + current_time_ms(), image=image_id,security_groups=[security_group['name']],
                                                    flavor=flavor, key_name=env['NOSE_KEYPAIR'], nics=nics)
    print(server)

    return server


def get_server(server_id):
    return get_cloud().nova_client.servers.get(server_id)


def destroy_server(server):
    get_cloud().nova_client.servers.delete(server)


def current_time_ms():
    return str(int(round(time.time() * 1000)))


def create_port_with_sg(security_group):
    network_id = env['NOSE_NET_ID']
    body_value = {'port': {
        'admin_state_up': True,
        'security_groups': [security_group['id']],
        'name': 'port-test'+current_time_ms(),
        'network_id': network_id,
    }}
    return get_cloud().neutron_client.create_port(body=body_value)



def get_console_log(server):
    return get_cloud().nova_client.servers.get(server.id).get_console_output(length=200)



def get_spice_console(server):
    return get_cloud().nova_client.servers.get(server.id).get_spice_console('spice-html5')


def create_server_snapshot(server):
    return get_cloud().nova_client.servers.create_image(server,server.name+current_time_ms())



def get_image(image_id):
    return get_cloud().glance_client.images.get(image_id)


def destroy_image(image_id):
    get_cloud().glance_client.images.delete(image_id)


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


def create_floating_ip():
    floating_ip = get_cloud().nova_client.floating_ips.create('public')
    return floating_ip


def associate_floating_ip_to_port(floating_ip, port):
    get_cloud().neutron_client.update_floatingip(floating_ip['id'],{'floatingip': {'port_id': port['id']}} )


def associate_floating_ip_to_server(floating_ip, server):
    get_cloud().nova_client.servers.get(server['id']).add_floating_ip(floating_ip['floating_ip_address'])


def create_security_group():
    return get_cloud().nova_client.security_groups.create(name="test"+current_time_ms(), description="Test image")


def delete_security_group(security_group):
    get_cloud().nova_client.security_groups.delete(security_group.id)


def delete_floating_ip(floating_ip):
    get_cloud().nova_client.floating_ips.delete(floating_ip.id)


def delete_port(port):
    get_cloud().neutron_client.delete_port(port.id)


def add_ssh_ingress_rule(security_group_id):
    get_cloud().nova_client.security_group_rules.create(security_group_id, ip_protocol="tcp",
                                                        from_port=22, to_port=22)

def create_volume():
    return get_cloud().cinder_client.volumes.create(5, name="test-volume")



def rescue(server):
    get_cloud().nova_client.servers.get(server.id).rescue()


def attach_volume_to_server(server,volume):

    return get_cloud().nova_client.volumes.create_server_volume(server.id, volume.id)


def detach_volume_from_server(server, volume):
    get_cloud().nova_client.delete_server_volume(server.id,volume.id)


def get_flavor_disk_size(flavor_id):
    return get_cloud().nova_client.flavors.get_flavor(flavor_id)


def hard_reboot(server):
    get_cloud().nova_client.servers.get(server.id).reboot(reboot_type='HARD')
    time.sleep(60)



def soft_reboot(server):
    get_cloud().nova_client.servers.get(server.id).reboot(reboot_type='SOFT')
    time.sleep(60)


#if __name__ == "__main__":
    #for i in  get_cloud().nova_client.servers.list():
    #    print i
    #security_group={}
    #security_group['name']="start-sg-start"
    #security_group['id']='e273c427-71e0-4e96-af1c-cc0ae88aee1d'
    #boot_vm(security_group)
    #test=get_image(env['NOSE_IMAGE_ID'])
    #print test.id
    #server=get_server("831ae819-84e0-4bcf-bc1d-a1327b4e7c74")
    #print server.name
    #destroy_server(test)

    #test=get_console_log(server)
    #print test
    #print get_spice_console(server)
    # create_server_snapshot(server)
    #create_floating_ip()
    #create_security_group()
    #get_cloud().neutron_client.delete_port("007265a6-cfa9-4db0-9af9-9e50519dcb6c")
    #test= get_cloud().neutron_client.update_floatingip('bd25fb62-a0e1-4087-b639-567ed955a7c9',{'floatingip': {'port_id': '9c2f9f57-18c9-40f5-b9a3-4f43d41bda1a'}})
    #create_volume()
    #get_cloud().nova_client.volumes.delete_server_volume("831ae819-84e0-4bcf-bc1d-a1327b4e7c74","8db4ed72-52f5-4d07-8d35-af925c4bd326")
    #print test
    #create_port_with_sg(security_group)
    #get_cloud().neutron_client.delete_port("605b7e4f-abde-4df0-9b58-abe532908a46")
    #keypair = get_cloud().nova_client.keypairs.create("testvm",public_key=file(test))
    #print(keypair)