import pytest

from DumbPipe import PipeExec


@pytest.fixture(scope='session', autouse=True)
def pipe():
    with PipeExec() as pipe:
        pipe.mail_subject = "Pipe Exec Testing"
        yield pipe


def test_error(pipe):
    with pytest.raises(ZeroDivisionError):
        pipe.execute((lambda x: x/0, [2]))


def test_push_notification(pipe):
    pipe.execute((pipe.notify, ["Title", "Message"], dict(timeout=0)))
