from plyer import notification

from DumbPipe.executor.interfaces import IConfig


class INotify(IConfig):
    def __init__(self, config_file=None):
        super(INotify, self).__init__(config_file)

    def notify(self, message, title=None, app_icon="", timeout=10):
        notification.notify(
            title=self.get_title(title),
            message=message,
            app_icon=app_icon,
            timeout=timeout
        )
