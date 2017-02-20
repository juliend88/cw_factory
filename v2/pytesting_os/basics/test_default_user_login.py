from basics import test_resources
import openstackutils

cwlib = openstackutils.OpenStackUtils()

def test_default_user_login():
    global test_resources
    ssh_connetion=cwlib.initiate_ssh(test_resources['my_floating'])
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_connetion.exec_command('pwd')
    ssh_user = ssh_stdout.read()
    print ssh_user
    search_user=ssh_user.find('/home/cloud') != -1

    assert search_user