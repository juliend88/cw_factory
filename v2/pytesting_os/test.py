#!/usr/bin/env python
#-*- coding: utf-8 -

from threading import Timer
import time
import openstackutils

'''
def timeout():
    print("Game over")

t = Timer(20, timeout)
t.start()

# do something else, such as
time.sleep(15)
'''


if __name__ == "__main__":

    c= openstackutils.OpenStackUtils()

    ser=c.get_server("5686cc09-8b5a-46ea-93c7-267f2e49701f")
    print c.unrescue(ser)
    print ser.status


    #while ser != 'ACTIVE':
    #    time.sleep(10)
    #    print "wait for server"
    #print "server is up"



