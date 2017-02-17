import time
from basics import test_resources
import openstackutils


cwlib = openstackutils.OpenStackUtils()


def test_rescue_unrescue():
    global test_resources
    rescue=cwlib.rescue(test_resources['my_server'])
    unrescue=cwlib.unrescue(test_resources['my_server'])

    assert rescue == 'RESCUE' and unrescue == 'ACTIVE'
