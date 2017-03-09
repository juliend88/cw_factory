from basics import test_resources

def test_no_visible_auth_error():
    global test_resources
    ssh_stdin, ssh_stdout, ssh_stderr = test_resources['ssh_connection'].exec_command('touch /tmp/toto.txt')
    auth_error = ssh_stdout.read()
    ssh_auth_error = (auth_error != -1)

    assert ssh_auth_error
