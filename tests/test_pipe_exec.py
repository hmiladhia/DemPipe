import pytest

from DumbPipe import PipeExecutor
from configDmanager.errors import ConfigNotFoundError


@pytest.fixture(scope='session', autouse=True)
def pipe():
    with PipeExecutor() as pipe:
        pipe.mail_subject = "Pipe Exec Testing"
        yield pipe


def test_default():
    with PipeExecutor(None) as p:
        p.execute((lambda x: x, [2]))


def test_config_not_found_error():
    with pytest.raises(ConfigNotFoundError):
        with PipeExecutor('TestConfig') as p:
            p.execute((lambda x: x, [2]))


def test_error(pipe):
    with pytest.raises(ZeroDivisionError):
        pipe.execute((lambda x: x/0, [2]))


def test_push_notification(pipe):
    pipe.execute((pipe.notify, ["Title", "Message"], dict(timeout=0)))
