#!/usr/bin/python

from StringIO import StringIO
import paramiko

class SshClient:
    "A wrapper of paramiko.SSHClient"
    TIMEOUT = 4

    def __init__(self, host,username,private_key_file):
        self.username=username
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, username=username, key_filename=private_key_file, timeout=180)

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def execute(self, command, sudo=False):
        if sudo and self.username != "root":
            command = "sudo -S -p '' %s" % command
        stdin, stdout, stderr = self.client.exec_command(command)
        return {'out': stdout.readlines(),
                'err': stderr.readlines(),
                'retval': stdout.channel.recv_exit_status()}

if __name__ == "__main__":
    client = SshClient(host='84.39.51.34',username='cloud',private_key_file='/home/mohamed/.ssh/alikey.pem')
    try:
        ret = client.execute('ls /', sudo=True)
        print "  ".join(ret["out"]), "  E ".join(ret["err"]), ret["retval"]
    finally:
        client.close()










#ssh_connex = paramiko.SSHClient()
#ssh_connex.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#ssh_connex.connect('84.39.51.34', username='cloud', key_filename='/home/mohamed/.ssh/alikey.pem', timeout=180)

#chan_in, chan_out, chan_err = ssh_connex.exec_command('lsblk | grep vda1 | awk \'{$1=" "; print $4}\'| tr -d "G"')

#data = chan_out.read()


#if data is not None:
#    print "n'est pas vide"
#else:
#    print "vide"
#if data.find("GNU Emacs") != -1:
#    print("SUCCESS "+str(data.find("GNU Emacs")))
#else:
#    print("FAILURE "+str(data.find("GNU Emacs")))
