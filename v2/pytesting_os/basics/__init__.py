import paramiko, time
import os_commons as cwlib


test_resources = {}


def setup():
    global test_resources
    start_chrono = int(round(time.time() * 1000))

    keypair = cwlib.create_keypair()
    security_group = cwlib.create_security_group()
    floating_ip = cwlib.create_floating_ip()

    server = cwlib.boot_vm(security_group,keypair)

    cwlib.associate_floating_ip_to_server(floating_ip, server)

    test_resources['my_keypair'] = keypair
    test_resources['my_server'] = server
    test_resources['my_sg'] = security_group
    test_resources['my_floating'] = floating_ip
    test_resources['ssh_connection'] = cwlib.initiate_ssh(floating_ip)
    stop_chrono = int(round(time.time() * 1000))

    print("Setup 'cloudinit' testsuite in " + str(stop_chrono - start_chrono) + " ms")


def teardown():
    global test_resources

    cwlib.destroy_server(test_resources['my_server'])
    cwlib.delete_security_group(test_resources['my_sg'])
    cwlib.delete_floating_ip(test_resources['my_floating'])
    cwlib.delete_keypair(test_resources['my_keypair'])