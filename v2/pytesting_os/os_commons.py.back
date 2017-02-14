import time, shade, re, paramiko
from os import environ as env
import novaclient.exceptions as nova_exceptions

shade.simple_logging()
cloud = None


def get_cloud():
    global cloud
    if not cloud:
        cloud = shade.OpenStackCloud(cloud='dc1')
    return cloud


def boot_vm_with_userdata_and_port(security_group, port, userdata_path):
    server = get_cloud().create_server("test-server-" + current_time_ms(),
                                       env['NOSE_IMAGE_ID'],
                                       env['NOSE_FLAVOR'],
                                       key_name=env['NOSE_KEYPAIR'],
                                       nics={'port-id': port['id']},
                                       security_groups=[security_group['name']],
                                       userdata=file(userdata_path),
                                       wait=True,
                                       timeout=600)
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


def boot_vm(security_group, image_id=env['NOSE_IMAGE_ID'], flavor=env['NOSE_FLAVOR']):
    server = get_cloud().create_server("test-server-" + current_time_ms(),
                                       image_id,
                                       flavor,
                                       key_name=env['NOSE_KEYPAIR'],
                                       nics={'net-id': env['FACTORY_NETWORK_ID']},
                                       security_groups=[security_group['name']],
                                       wait=True,
                                       timeout=600)
    wait_for_cloud_init(server)

    return server


def get_server(server_id):
    try:
        return get_cloud().get_server_by_id(server_id)
    except nova_exceptions.NotFound:
        return None


def destroy_server(server):
    get_cloud().delete_server(server['id'])
    server = get_server(server['id'])
    server_name = server['name']
    counter = 0
    while server and counter < 30:
        time.sleep(6)
        server = get_server(server['id'])
        counter += 1
    print("Destroyed server " + str(server_name) + " (detected suppression after " + str(counter * 6) + " seconds)")


def current_time_ms():
    return str(int(round(time.time() * 1000)))


def create_port_with_sg(security_group):
    target_network = env['FACTORY_NETWORK_ID']
    return get_cloud().create_port(target_network, security_groups=[security_group['id']])


def get_console_log(shade_server):
    nova_server = get_cloud().nova_client.servers.get(shade_server['id'])
    return nova_server.get_console_output(length=200)


def get_spice_console(shade_server):
    nova_server = get_cloud().nova_client.servers.get(shade_server['id'])
    return nova_server.get_spice_console('spice-html5')


def create_server_snapshot(shade_server):
    snapshot_name = 'test_snapshot-' + shade_server['name']
    nova_server = get_cloud().nova_client.servers.get(shade_server['id'])

    snapshot_image_id = get_cloud().nova_client.servers.create_image(nova_server, snapshot_name)

    snapshot_image = get_image(snapshot_image_id)
    counter = 0
    while snapshot_image['status'] != 'active' and counter < 30:
        time.sleep(6)
        snapshot_image = get_image(snapshot_image_id)
        counter += 1

    print("Created snapshot image in " + str(counter * 6) + " sec")

    return snapshot_image


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
    return get_cloud().get_image(image_id)


def create_floating_ip():
    return get_cloud().create_floating_ip(network='public')


def associate_floating_ip_to_port(floating_ip, port):
    neutron_client = get_cloud().neutron_client
    neutron_client.update_floatingip(floating_ip['id'], {'floatingip': {'port_id': port['id']}})


def associate_floating_ip_to_server(floating_ip, server):
    nova_client = get_cloud().nova_client
    nova_client.servers.get(server['id']).add_floating_ip(floating_ip['floating_ip_address'])


def create_security_group():
    new_security_group = get_cloud().create_security_group("test-sg-" + current_time_ms(),
                                                           "Tmp security group for testing")
    add_ssh_ingress_rule(new_security_group['id'])

    return get_cloud().get_security_group(new_security_group['id'])


def delete_security_group(security_group):
    get_cloud().delete_security_group(security_group['id'])


def delete_floating_ip(floating_ip):
    get_cloud().delete_floating_ip(floating_ip['id'])


def delete_port(port):
    get_cloud().delete_port(port['id'])


def add_ssh_ingress_rule(security_group_id):
    get_cloud().create_security_group_rule(security_group_id,
                                           port_range_min=22,
                                           port_range_max=22,
                                           protocol='TCP')


def create_volume():
    created_volume = get_cloud().create_volume(5, True, 180)
    return created_volume


def rescue(shade_server):
    nova_client = get_cloud().nova_client
    nova_client.servers.get(shade_server['id']).rescue()


def attach_volume_to_server(shade_server, shade_volume):
    get_cloud().attach_volume(shade_server, shade_volume, '/dev/vdb', True, 180)
    return get_cloud().get_volume(shade_volume['id'])


def detach_volume_from_server(shade_server, shade_volume):
    get_cloud().detach_volume(shade_server, shade_volume, True, 180)


def get_flavor_disk_size(flavor_id):
    return get_cloud().get_flavor(flavor_id)


def hard_reboot(shade_server):
    nova_client = get_cloud().nova_client
    nova_client.servers.get(shade_server['id']).reboot(reboot_type='HARD')
    time.sleep(60)
    wait_for_cloud_init(shade_server)


def soft_reboot(shade_server):
    nova_client = get_cloud().nova_client
    nova_client.servers.get(shade_server['id']).reboot(reboot_type='SOFT')
    time.sleep(60)
    wait_for_cloud_init(shade_server)
