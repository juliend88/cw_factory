import time
import os_commons as cwlib
from basics import test_resources



def test_volume_attachment():
    global test_resources
    cwlib.attach_volume_to_server(test_resources['my_server'])
    time.sleep(60)
    ssh_stdin, ssh_stdout, ssh_stderr = test_resources['ssh_connection'].exec_command('ls /dev/vdb')
    device_file_listing = ssh_stdout.read()

    assert device_file_listing.find('/dev/vdb') != -1

    cwlib.detach_volume_from_server(test_resources['my_server'])
