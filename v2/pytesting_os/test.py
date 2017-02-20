#!/usr/bin/env python
#-*- coding: utf-8 -
import time, paramiko,os
from os import environ as env


def initiate_ssh(floating_ip):
    counter = 0
    while counter < 50:
        counter += 1
        try:
            ssh_connection = paramiko.SSHClient()
            ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_connection.connect(
                floating_ip,
                username='cloud',
                key_filename= env['HOME']+'/.ssh/alikey.pem',
                timeout=1000)
            return ssh_connection
            print 'connexion ssh'
        except paramiko.ssh_exception.NoValidConnectionsError:
            time.sleep(6)
            pass

    return None



if __name__ == "__main__":

   test =initiate_ssh('84.39.37.80')
   print test
   ssh_stdin, ssh_stdout, ssh_stderr = test.exec_command('df -h')
   ssh_hostname = ssh_stdout.read()
   ss = ssh_hostname.find('/hujmkj')
   print ss