import os_commons as cwlib
from basics import test_resources
from dateutil.parser import parse as parse_date


def test_hard_reboot():
    last_boot_before_reboot = get_last_boot_date()

    cwlib.hard_reboot(test_resources['my_server'])

    test_resources['ssh_connection'] = cwlib.initiate_ssh(test_resources['my_floating'],test_resources['my_keypair'])

    last_boot_after_reboot = get_last_boot_date()

    assert last_boot_before_reboot < last_boot_after_reboot


def test_soft_reboot():
    last_boot_before_reboot = get_last_boot_date()

    cwlib.soft_reboot(test_resources['my_server'])

    test_resources['ssh_connection'] = cwlib.initiate_ssh(test_resources['my_floating'],test_resources['my_keypair'])

    last_boot_after_reboot = get_last_boot_date()

    assert last_boot_before_reboot < last_boot_after_reboot


def get_last_boot_date():
    ssh_stdin, ssh_stdout, ssh_stderr = test_resources['ssh_connection'].exec_command(
        'who -b | tr -s " " | cut -d" " -f4,5')
    return parse_date(ssh_stdout.read())
