#!/usr/bin/env python
import time, paramiko,os,re,errno
from socket import error as socket_error
from openstackutils.openstackutils import OpenStackUtils
from os import environ as env
from dateutil.parser import parse as parse_date

cwlib =OpenStackUtils()

'''

def get_last_boot_date():
    ssh_connex = paramiko.SSHClient()
    ssh_connex.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connex.connect('84.39.39.205', username='cloud', key_filename='/home/mohamed/.ssh/alikey.pem', timeout=180)
    chan_in, chan_out, chan_err = ssh_connex.exec_command(
        'who -b | tr -s " " | cut -d" " -f4,5')
    return parse_date(chan_out.read())

'''


#if __name__ == '__main__':

    #port= cwlib.create_port_with_sg() 688099dc-1cff-4dde-bfd9-13de09e972bf

    #print port['port']['id']

    #cwlib.delete_port(port)

    #key,file=cwlib.create_keypair()

    #print key.__dict__
    #print file

    #cwlib.nova_client.keypairs.delete('nose_keypair1488277964336')
    #cwlib.nova_client.floating_ips.delete('c40920a2-f988-4ab3-bc61-dd40057c1c2c')
    #cwlib.delete_keypair("nose_keypair1488277818448","/home/mohamed/key-1488277818448.pem")
    #cwlib.delete_keypair('nose_keypair1488277951944','/home/mohamed/key-1488277951944.pem')

    server=cwlib.get_server('24def60d-858c-4c05-a8ce-44b86c1a270b')

    #print "__________________soft reboot__________________________"
    #print get_last_boot_date()
    #cwlib.server_reboot(server,'SOFT')
    #print server.status
    #cwlib.wait_server_is_up(server)

    #print get_last_boot_date()
    #print '__________________hard reboot__________________________'
    #cwlib.server_reboot(server,'HARD')
    #print server.status
    #cwlib.wait_server_is_up(server)
    #print get_last_boot_date()