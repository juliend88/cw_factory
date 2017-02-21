import time
from basics import test_resources
import openstackutils
from basics import test_resources


cwlib = openstackutils.OpenStackUtils()

def test_boot_snapshot_in_other_flavor():
    global test_resources

    snapshot_image = cwlib.create_server_snapshot(test_resources['my_server'])

    print "the id of snapshot is:"+snapshot_image

    cwlib.wait_server_available(test_resources['my_server'])

    new_server = cwlib.boot_vm(image_id=snapshot_image, flavor=17,keypair=test_resources['my_keypair'])

    floating = cwlib.create_floating_ip()
    cwlib.associate_floating_ip_to_server(floating, new_server)
    time.sleep(20)
    ssh_connection = cwlib.initiate_ssh(floating)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command('sudo ls /home')
    ssh_test = ssh_stdout.read()
    test_boot_snapshot=(ssh_test.find('cloud') != -1)

    assert test_boot_snapshot

    cwlib.destroy_server(new_server)

    cwlib.destroy_image(snapshot_image)

    cwlib.delete_floating_ip(floating)
