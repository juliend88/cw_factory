from cloudinit import test_resources


def test_cloudinit_runcmd():
    global test_resources

    ssh_stdin, ssh_stdout, ssh_stderr = test_resources['ssh_connection'].exec_command('sudo ls /root/')

    file_created_by_userdata_is_present = (ssh_stdout.read().find('cloud-init.txt') != -1)

    assert file_created_by_userdata_is_present


def test_cloudinit_package():
    global test_resources

    ssh_stdin, ssh_stdout, ssh_stderr = test_resources['ssh_connection'].exec_command('emacs --version')

    cmd_stdout = ssh_stdout.read()
    package_installed_by_userdata_is_present = (cmd_stdout.find('GNU Emacs') != -1)

    print("Expecting to find 'GNU Emacs' in:\n" + cmd_stdout)

    assert package_installed_by_userdata_is_present

