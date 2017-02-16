import os_commons as cwlib
from basics import test_resources
import re

def test_console_log():
    global test_resources

    console_log = cwlib.get_console_log(test_resources['my_server'])

    assert re.search(r'^.*Cloud-init .* finished.*$',console_log, flags=re.MULTILINE)
