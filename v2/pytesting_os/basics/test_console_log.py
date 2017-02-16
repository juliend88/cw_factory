import os_commons as cwlib
from basics import test_resources
import time

def test_console_log():
    global test_resources

    print test_resources['my_server'].id

    console_log = cwlib.get_console_log(test_resources['my_server'])

    time.sleep(20)

    #console_log_result= re.search(r'^.*Cloud-init .* finished.*$',console_log, flags=re.MULTILINE) !=-1

    assert console_log.find('Cloud-init') != -1