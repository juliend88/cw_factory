'''
import os, paramiko, time, paramiko.ssh_exception
import openstackutils



cwlib = openstackutils.OpenStackUtils()
test_resources = {}


def setup():
    global test_resources
    start_chrono = int(round(time.time() * 1000))

    floating_ip = cwlib.create_floating_ip()
    cwlib.associate_floating_ip_to_port(floating_ip)
    userdata_path = os.path.dirname(os.path.realpath(__file__)) + '/userdata.yml'
    server = cwlib.boot_vm_with_userdata_and_port(userdata_path)

    test_resources['my_floating'] = floating_ip
    test_resources['ssh_connection'] = cwlib.initiate_ssh(floating_ip)
    test_resources['my_server'] = server

    stop_chrono = int(round(time.time() * 1000))

    print("Setup 'cloudinit' testsuite in " + str(stop_chrono - start_chrono) + " ms")


#def teardown():
#    global test_resources
#    cwlib.destroy_server(test_resources['my_server'])
#    cwlib.delete_floating_ip(test_resources['my_floating'])

'''