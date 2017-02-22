#!/usr/bin/env python

import openstackutils as c

cwlib =c.OpenStackUtils()





if __name__ == '__main__':

    port= cwlib.create_port_with_sg()

    print port['port']['id']

    cwlib.delete_port(port)