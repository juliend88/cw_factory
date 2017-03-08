from basics import test_resources,cwlib


def test_spice_console():
    global test_resources
    spice_console_url = cwlib.get_spice_console(test_resources['my_server'])

    assert spice_console_url['console']['url'].startswith('https://')
