from basics import test_resources,cwlib

def test_console_log():
    global test_resources

    console_log = cwlib.get_console_log(test_resources['my_server'])

    assert console_log is not None
