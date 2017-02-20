from os import environ as env
from basics import test_resources
import openstackutils


cwlib = openstackutils.OpenStackUtils()

global test_resources

def test_disk_size():

    expected_disk_size = str(cwlib.get_flavor_disk_size(env['NOSE_FLAVOR'])).strip()
    ssh_connetion=cwlib.initiate_ssh(test_resources['my_floating'])
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_connetion.exec_command(
        'df -h | grep /dev/vda1 | tr -s " " | cut -d" " -f2 | tr -d "G"')

    actual_disk_size = str(ssh_stdout.read()).strip()

    print("EXPECTED '" + str(expected_disk_size) + "' vs ACTUAL '" + str(actual_disk_size)+"'")

    assert expected_disk_size == actual_disk_size
