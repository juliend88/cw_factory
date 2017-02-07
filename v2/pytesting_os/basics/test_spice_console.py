import os_commons as cwlib
from basics import test_resources


def test_spice_console():
    spice_console_url = cwlib.get_spice_console(test_resources['my_server'])

    assert spice_console_url['console']['url'].startswith('https://')
