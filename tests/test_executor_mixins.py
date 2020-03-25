import pytest

from DemPipe.executor import PushNotificationMixin


class NotifyExecutor(PushNotificationMixin):
    def __init__(self, config_file=r'DemPipe.PipeConfig'):
        super(NotifyExecutor, self).__init__(config_file=config_file)


@pytest.fixture(scope='session', autouse=True)
def pipe():
    with NotifyExecutor() as pipe:
        yield pipe


def test_push_notification(mocker, pipe):
    mocked_notify = mocker.patch('plyer.notification.notify')
    pipe.execute((pipe.notify, ["Message", "Title"], dict(timeout=0)))
    mocked_notify.assert_called_with(title="[Pipe Execution] - Title", message="Message",
                                     timeout=0, app_icon='')
