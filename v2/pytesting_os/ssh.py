import os, paramiko

ssh_connex = paramiko.SSHClient()
ssh_connex.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_connex.connect('84.39.34.176', username='cloud', key_filename='/Users/amaury/.ssh/amaury-ext-compute.pem', timeout=180)

chan_in, chan_out, chan_err = ssh_connex.exec_command("emacs --version")

data = chan_out.read()
if data.find("GNU Emacs") != -1:
    print("SUCCESS "+str(data.find("GNU Emacs")))
else:
    print("FAILURE "+str(data.find("GNU Emacs")))
