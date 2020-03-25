import traceback

from DemPipe.executor.mixin import EmailMixin


class PipeExecutor(EmailMixin):
    def __init__(self, config_file=r'DemPipe.PipeConfig'):
        super(PipeExecutor, self).__init__(config_file=config_file)

    # Handler
    def _get_error_message(self, exception, tb) -> str:
        return "# Traceback\n" + '\n\n'.join(map(lambda x: f'<span style="color: red;">{x}</span>', tb.split('\n')))

    def _get_error_subject(self, exception) -> str:
        return f'Failed: {exception}'

    def handler(self, action, exception, *args, **kwargs):
        if self.mail_default_receiver and self.mail_is_configured():
            tb = traceback.format_exc()
            message = self._get_error_message(exception, tb)
            subject = self._get_error_subject(exception)
            self.send_mail(message, self.mail_default_receiver, subject)
        return super(PipeExecutor, self).handler(action, exception, *args, **kwargs)