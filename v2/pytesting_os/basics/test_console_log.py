from basics import test_resources
import time
import openstackutils


cwlib = openstackutils.OpenStackUtils()

def test_console_log():
    global test_resources

    console_log = cwlib.get_console_log(test_resources['my_server'])

    time.sleep(20)

    assert console_log.find('Cloud-init') != -1