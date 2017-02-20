from basics import test_resources
import openstackutils


cwlib = openstackutils.OpenStackUtils()



def test_local_name_resolution():
    global test_resources
    ssh_connetion=cwlib.initiate_ssh(test_resources['my_floating'])
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_connetion.exec_command('sudo ls 2>&1')
    ssh_local_name_resolution = ssh_stdout.read()
    validate_local_resolution = ssh_local_name_resolution.find('unable to resolve host') == -1

    assert validate_local_resolution
