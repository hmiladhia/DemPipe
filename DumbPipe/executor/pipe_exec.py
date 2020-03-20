import traceback

from DumbPipe.executor import PipeExecutorBase
from DumbPipe.executor.interfaces import IMail, INotify


class PipeExecutor(PipeExecutorBase, IMail, INotify):
    def __init__(self, config_file=r'DumbPipe.PipeConfig'):
        super(PipeExecutor, self).__init__()
        IMail.__init__(self, config_file)
        INotify.__init__(self, config_file)

    # Actions
    def quit(self, exc_type, exc_val, exc_tb):
        super(PipeExecutor, self).quit(exc_type, exc_val, exc_tb)
        if exc_type:
            self.notify(str(exc_val), 'Error')
        else:
            self.notify('Ran Successfully')

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