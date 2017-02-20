from basics import test_resources
import openstackutils


cwlib = openstackutils.OpenStackUtils()

def test_no_visible_auth_error():
    global test_resources
    ssh_connetion=cwlib.initiate_ssh(test_resources['my_floating'])
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_connetion.exec_command('cat /var/log/auth.log')
    auth_error = ssh_stdout.read()
    ssh_auth_error = auth_error.find('error') == -1

    assert ssh_auth_error
