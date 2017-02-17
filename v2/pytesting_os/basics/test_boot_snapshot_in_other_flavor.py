import time
from basics import test_resources
import openstackutils


cwlib = openstackutils.OpenStackUtils()

def test_boot_snapshot_in_other_flavor():
    global test_resources

    snapshot_image = cwlib.create_server_snapshot(test_resources['my_server'])

    print "the id of snapshot is:"+snapshot_image

    new_server = cwlib.boot_vm(image_id=snapshot_image, flavor=21)

    floating = cwlib.create_floating_ip()

    cwlib.associate_floating_ip_to_server(floating, new_server)

    ssh_connection = cwlib.initiate_ssh(floating)

    assert ssh_connection

    cwlib.destroy_server(new_server)

    cwlib.destroy_image(snapshot_image)
