from basics import test_resources,cwlib

def test_volume_attachment():

    cwlib.attach_volume_to_server(test_resources['my_server'],test_resources['my_volume'])

    ssh_stdin, ssh_stdout, ssh_stderr = test_resources['ssh_connection'].exec_command('lsblk')

    device_file_listing = ssh_stdout.read()

    print device_file_listing

    assert device_file_listing.find('vdb') != -1

    cwlib.detach_volume_from_server(test_resources['my_server'],test_resources['my_volume'])
