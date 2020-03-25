from plyer import notification

from DemPipe.executor.mixin import ConfigMixin


class PushNotificationMixin(ConfigMixin):
    def __init__(self, config_file=None):
        super(PushNotificationMixin, self).__init__(config_file)

    def notify(self, message, title=None, app_icon="", timeout=10):
        notification.notify(
            title=self.get_title(title),
            message=message,
            app_icon=app_icon,
            timeout=timeout
        )

    # Actions
    def _quit(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.notify(str(exc_val), 'Error')
