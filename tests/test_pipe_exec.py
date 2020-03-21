import os

import pytest

from configDmanager.errors import ConfigNotFoundError

from DumbPipe import PipeExecutor


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


def test_error(monkeypatch, mocker, pipe):
    err_msg = 'zero division error message'
    monkeypatch.setattr(pipe, '_get_error_message', lambda x, y: err_msg, raising=True)
    mocker.spy(pipe, 'send_mail')

    with pytest.raises(ZeroDivisionError):
        pipe.execute((lambda x: x/0, [2]))

    assert pipe.send_mail.call_count == 1
    pipe.send_mail.assert_called_with(err_msg, os.environ.get('receiver'), 'Failed: division by zero')


def test_push_notification(pipe):
    pipe.execute((pipe.notify, ["Title", "Message"], dict(timeout=0)))
