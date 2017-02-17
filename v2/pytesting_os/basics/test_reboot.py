from basics import test_resources
from dateutil.parser import parse as parse_date
import time
import openstackutils


cwlib = openstackutils.OpenStackUtils()


def test_hard_reboot():
    global test_resources
    last_boot_before_reboot = get_last_boot_date()
    cwlib.hard_reboot(test_resources['my_server'])
    test_resources['ssh_connection'] = cwlib.initiate_ssh(test_resources['my_floating'])

    last_boot_after_reboot = get_last_boot_date()

    assert last_boot_before_reboot < last_boot_after_reboot


def test_soft_reboot():
    global test_resources
    last_boot_before_reboot = get_last_boot_date()
    cwlib.soft_reboot(test_resources['my_server'])
    test_resources['ssh_connection'] = cwlib.initiate_ssh(test_resources['my_floating'])

    last_boot_after_reboot = get_last_boot_date()

    assert last_boot_before_reboot < last_boot_after_reboot


def get_last_boot_date():
    global test_resources
    ssh_stdin, ssh_stdout, ssh_stderr = test_resources['ssh_connection'].exec_command(
        'who -b | tr -s " " | cut -d" " -f4,5')
    return parse_date(ssh_stdout.read())
