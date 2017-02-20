#!/usr/bin/env python
import os, paramiko

ssh_connex = paramiko.SSHClient()
ssh_connex.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_connex.connect('84.39.39.81', username='cloud', key_filename='/home/mohamed/.ssh/key.pem', timeout=180)

chan_in, chan_out, chan_err = ssh_connex.exec_command("cat /etc/passwd")

data = chan_out.read()

print len(data)

if data is not None:
    print "n'est pas vide"
else:
    print "vide"
#if data.find("GNU Emacs") != -1:
#    print("SUCCESS "+str(data.find("GNU Emacs")))
#else:
#    print("FAILURE "+str(data.find("GNU Emacs")))
