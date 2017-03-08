import time
from basics import test_resources,cwlib
from dateutil.parser import parse as parse_date


def test_hard_reboot():

    last_boot_before_reboot = get_last_boot_date()

    cwlib.server_reboot(test_resources['my_server'],'HARD')

    last_boot_after_reboot = get_last_boot_date()

    assert last_boot_before_reboot < last_boot_after_reboot




def test_soft_reboot():

    last_boot_before_reboot = get_last_boot_date()

    cwlib.server_reboot(test_resources['my_server'],'SOFT')

    last_boot_after_reboot = get_last_boot_date()

    assert last_boot_before_reboot < last_boot_after_reboot


def get_last_boot_date():
    ssh_connection=cwlib.initiate_ssh(test_resources['my_floating'],test_resources['my_private_key'])
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command(
        'who -b | tr -s " " | cut -d" " -f4,5')
    date = parse_date(ssh_stdout.read())
    cwlib.close_ssh_connextion(ssh_connection)
    return date
