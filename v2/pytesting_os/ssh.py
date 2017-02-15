#!/usr/bin/env python
import os, paramiko

ssh_connex = paramiko.SSHClient()
ssh_connex.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_connex.connect('84.39.44.215', username='cloud', key_filename='/home/mohamed/.ssh/alikey.pem', timeout=180)

chan_in, chan_out, chan_err = ssh_connex.exec_command("cat /etc/passwd")

print ssh_connex
data = chan_out.read()

print data
#if data.find("GNU Emacs") != -1:
#    print("SUCCESS "+str(data.find("GNU Emacs")))
#else:
#    print("FAILURE "+str(data.find("GNU Emacs")))
