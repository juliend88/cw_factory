from basics import test_resources
import openstackutils


cwlib = openstackutils.OpenStackUtils()

def test_haveged_running():
    global test_resources
    ssh_connetion=cwlib.initiate_ssh(test_resources['my_floating'])
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_connetion.exec_command(
        'ps aux | grep haveged | grep -v grep')
    ssh_haveged = ssh_stdout.read()
    haveged_running = ssh_haveged.find('sbin/haveged') != -1

    assert haveged_running
