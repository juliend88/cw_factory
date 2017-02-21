#!/usr/bin/env python

import openstackutils as c

cwlib =c.OpenStackUtils()





if __name__ == '__main__':


    server=cwlib.get_server()
    server