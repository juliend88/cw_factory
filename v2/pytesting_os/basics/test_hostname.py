from basics import test_resources
import openstackutils



cwlib = openstackutils.OpenStackUtils()

def test_hostname():
    global test_resources

    hostname = test_resources['my_server'].name
    ssh_connetion=cwlib.initiate_ssh(test_resources['my_floating'])
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_connetion.exec_command('hostname')
    ssh_hostname = ssh_stdout.read()
    print("Expected hostname="+hostname)
    print("Found hostname="+ssh_hostname)
    hostname_result_compare = ssh_hostname.find(hostname) != -1

    assert hostname_result_compare
