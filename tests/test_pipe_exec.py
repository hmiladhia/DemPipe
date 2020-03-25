import os

import pytest

from configDmanager.errors import ConfigNotFoundError

from DemPipe import PipeExecutor


@pytest.fixture(scope='session', autouse=True)
def pipe():
    with PipeExecutor() as pipe:
        pipe.pipe_name = "Pipe Exec Testing"
        yield pipe


def test_default():
    with PipeExecutor(None) as p:
        p.execute((lambda x: x, [2]))


def test_config_not_found_error():
    with pytest.raises(ConfigNotFoundError):
        with PipeExecutor('TestConfig') as p:
            p.execute((lambda x: x, [2]))


def test_error(mocker, pipe):
    err_msg = 'zero division error message'
    mocker.patch.object(pipe, '_get_error_message', lambda x, y: err_msg)
    mocked_send_message = mocker.patch('Dmail.Email.send_message')

    with pytest.raises(ZeroDivisionError):
        pipe.execute((lambda x: x/0, [2]))

    assert mocked_send_message.call_count == 1
    mocked_send_message.assert_called_with(err_msg, os.environ.get('receiver'),
                                           '[Pipe Exec Testing] - Failed: division by zero', cc=None, bcc=None,
                                           subtype='md', attachments=None)