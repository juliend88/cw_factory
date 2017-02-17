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
    server=c.get_server("cedf00b0-0b44-41a7-a02f-9f43467c26bb")
    #print c.get_console_log(server)
    rescue=c.rescue(server)
    print type(rescue)
    #print getattr(server,'OS-EXT-STS:task_state')
    #img=c.create_server_snapshot(server)
    #print img
    #image=c.get_image(img)
    #print image.status


    #while ser != 'ACTIVE':
    #    time.sleep(10)
    #    print "wait for server"
    #print "server is up"



