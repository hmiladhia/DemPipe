import pytest

from DemPipe import PipeExecutorBase
from DemPipe.executor import PushNotificationMixin


class NotifyExecutor(PipeExecutorBase, PushNotificationMixin):
    def __init__(self, config_file=r'DemPipe.PipeConfig'):
        super(NotifyExecutor, self).__init__()
        PushNotificationMixin.__init__(self, config_file)


@pytest.fixture(scope='session', autouse=True)
def pipe():
    with NotifyExecutor() as pipe:
        pipe.pipe_name = "Notify Executor Testing"
        yield pipe


def test_push_notification(mocker, pipe):
    mocked_notify = mocker.patch('plyer.notification.notify')
    pipe.execute((pipe.notify, ["Message", "Title"], dict(timeout=0)))
    mocked_notify.assert_called_with(title="[Notify Executor Testing] - Title", message="Message",
                                     timeout=0, app_icon='')
