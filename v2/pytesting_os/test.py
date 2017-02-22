#!/usr/bin/env python

import openstackutils as c

cwlib =c.OpenStackUtils()





if __name__ == '__main__':

    print cwlib.create_port_with_sg()
