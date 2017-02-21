import os_commons as cwlib
from basics import test_resources


def test_boot_snapshot_in_other_flavor():
    global test_resources

    snapshot_image = cwlib.create_server_snapshot(test_resources['my_server'])

    new_server = cwlib.boot_vm(test_resources['my_sg'], snapshot_image['id'], 17)
    floating = cwlib.create_floating_ip(test_resources['my_floating'])
    cwlib.associate_floating_ip_to_server(floating, new_server)

    ssh_connection = cwlib.initiate_ssh(floating)

    assert ssh_connection

    cwlib.destroy_server(new_server)

    cwlib.destroy_image(snapshot_image['id'])
