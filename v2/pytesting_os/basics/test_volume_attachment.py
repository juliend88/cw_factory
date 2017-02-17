import time
from basics import test_resources
import openstackutils


cwlib = openstackutils.OpenStackUtils()


def test_volume_attachment():
    global test_resources
    att=cwlib.attach_volume_to_server(test_resources['my_server'])
    print att
    time.sleep(60)
    ssh_stdin, ssh_stdout, ssh_stderr = test_resources['ssh_connection'].exec_command('ls /dev/')
    device_file_listing = ssh_stdout.read()

    print device_file_listing

    assert device_file_listing.find('/dev/vdb') != -1

    cwlib.detach_volume_from_server(test_resources['my_server'])
