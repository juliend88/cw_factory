#!/usr/bin/env python
#-*- coding: utf-8 -*-
from openstackutils import OpenStackUtils
import time, re, paramiko, os
from os import environ as env



def get_cloud():
    return OpenStackUtils()


def boot_vm_with_userdata_and_port(security_group,keypair, port,userdata_path):
    nics = [{'port-id': port['port']['id']}]
    server = get_cloud().nova_client.servers.create(name="test-server-" + current_time_ms(), image=env['NOSE_IMAGE_ID'],security_groups=[security_group.name],
                                                    flavor=env['NOSE_FLAVOR'], key_name=keypair.id, userdata=file(userdata_path), nics=nics)

    wait_for_cloud_init(server)

    return server


def boot_vm(security_group,keypair,image_id=env['NOSE_IMAGE_ID'],flavor=env['NOSE_FLAVOR']):
    nics = [{'net-id': env['NOSE_NET_ID']}]
    server = get_cloud().nova_client.servers.create(name="test-server-" + current_time_ms(), image=image_id,security_groups=[security_group.name],
                                                    flavor=flavor, key_name=keypair.id, nics=nics)

    wait_for_cloud_init(server)

    return server


def wait_for_cloud_init(server):
    counter = 0
    while counter < 100:
        console_log = get_console_log(server)
        if re.search('^.*Cloud-init .* finished.*$', console_log, flags=re.MULTILINE):
            print("Cloudinit finished in " + str(counter * 6))
            return
        time.sleep(6)
        counter += 1
    print("Cloudinit end not detected in " + str(counter * 6))



def get_server(server_id):
    return get_cloud().nova_client.servers.get(server_id)


def destroy_server(server):
    get_cloud().nova_client.servers.delete(server)


def current_time_ms():
    return str(int(round(time.time() * 1000)))


def create_port_with_sg(security_group):
    try:
       network_id = env['NOSE_NET_ID']
       body_value = {'port': {
         'admin_state_up': True,
         'security_groups': [security_group.id],
         'name': 'port-test'+current_time_ms(),
         'network_id': network_id,
                              }}
       response = get_cloud().neutron_client.create_port(body=body_value)
       print(response)
    finally:
        print("Execution cmpleted")

    return response


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
                floating_ip.floating_ip_address,
                username='cloud',
                key_filename=env['HOME']+'/private_key.pem',
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
    get_cloud().neutron_client.update_floatingip(floating_ip.id,{'floatingip': {'port_id': port['port']['id'] }})


def associate_floating_ip_to_server(floating_ip, server):
    get_cloud().nova_client.servers.get(server.id).add_floating_ip(floating_ip.ip)


def create_security_group():
    security_group=get_cloud().nova_client.security_groups.create(name="test"+current_time_ms(), description="Test image")
    add_ssh_ingress_rule(security_group.id)
    return security_group


def delete_security_group(security_group):
    get_cloud().nova_client.security_groups.delete(security_group.id)


def delete_floating_ip(floating_ip):
    get_cloud().nova_client.floating_ips.delete(floating_ip.id)


def delete_port(port):
    get_cloud().neutron_client.delete_port(port['port']['id'])


def add_ssh_ingress_rule(security_group_id):
    get_cloud().nova_client.security_group_rules.create(security_group_id, ip_protocol="tcp",
                                                        from_port=22, to_port=22)

def create_volume():
    return get_cloud().cinder_client.volumes.create(5, name="test-volume"+current_time_ms())



def rescue(server):
    get_cloud().nova_client.servers.get(server.id).rescue()


def attach_volume_to_server(server,volume):
    return get_cloud().nova_client.volumes.create_server_volume(server.id, volume.id)


def detach_volume_from_server(server, volume):
    get_cloud().nova_client.delete_server_volume(server.id,volume.id)


def get_flavor_disk_size(flavor_id):
    return get_cloud().nova_client.flavors.get(flavor_id).disk



def hard_reboot(server):
    get_cloud().nova_client.servers.get(server.id).reboot(reboot_type='HARD')
    time.sleep(60)



def soft_reboot(server):
    get_cloud().nova_client.servers.get(server.id).reboot(reboot_type='SOFT')
    time.sleep(60)


def create_keypair():
    keypair = get_cloud().nova_client.keypairs.create("testkeypair"+current_time_ms())
    fp = os.open(env['HOME']+"/private_key.pem", os.O_WRONLY | os.O_CREAT, 0o600)
    with os.fdopen(fp, 'w') as f:
     f.write(keypair.private_key)
    return keypair


def delete_keypair(keypair):
    get_cloud().nova_client.keypairs.delete(keypair.id)


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
    #k=create_keypair()
    #print k.name
    #print k.id
    #test= get_cloud().nova_client.flavors.get(env['NOSE_FLAVOR'])
    #print (test.disk)
    #spice_console_url = get_cloud().nova_client.servers.get("7b1ee4b2-b9b2-4dbb-9ff8-ace6788ee335").get_spice_console('spice-html5')
    #Test= spice_console_url['console']['url'].startswith('https://')
    #print Test
    #boot_vm_with_userdata_and_port(security_group,keypair , port, userdata_path)
    #test=create_floating_ip()
    #print(test.__dict__)
    #get_cloud().nova_client.servers.get("e81825e0-a211-4a9f-9c1a-e4335409ca88").add_floating_ip(test.ip)
    #security_group=create_security_group()
    #print security_group.id
    #floating_ip = create_floating_ip()
    #port = create_port_with_sg(security_group)
    #print port['port']['id']
    #associate_floating_ip_to_port(floating_ip, port)
    #associate_floating_ip_to_port(floating_ip, port)
    #network_id = env['NOSE_NET_ID']
    #body_value = {'port': {
    #    'admin_state_up': True,
    #    'security_groups': ["e273c427-71e0-4e96-af1c-cc0ae88aee1d"],
    #    'name': 'port-testnpppppppppppppp',
    #    'network_id': network_id,
    #}}
    #get_cloud().neutron_client.create_port(body=body_value)
