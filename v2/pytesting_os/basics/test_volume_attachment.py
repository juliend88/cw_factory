from basics import test_resources
import openstackutils

cwlib = openstackutils.OpenStackUtils()

def test_volume_attachment():
    global test_resources

    cwlib.attach_volume_to_server(test_resources['my_server'])

    ssh_connetion=cwlib.initiate_ssh(test_resources['my_floating'])

    ssh_stdin, ssh_stdout, ssh_stderr = ssh_connetion.exec_command('ls /dev/vdb')

    device_file_listing = ssh_stdout.read()

    assert device_file_listing.find('/dev/vdb') != -1

    cwlib.detach_volume_from_server(test_resources['my_server'])
