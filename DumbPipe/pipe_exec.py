import os
import traceback

from configDmanager import import_config, Config
from configDmanager.errors import ConfigNotFoundError
from Dmail import Email
from plyer import notification

from DumbPipe._action_base import ActionBase
from DumbPipe._pipe import DPipeExec


class PipeExec(DPipeExec):
    mail_default_receiver: str
    mail_subject: str
    mail_use_tls: bool
    mail_password: str
    mail_user: str
    mail_port: int
    mail_server: str

    def __init__(self, config_file=r'config.PipeConfig'):
        super(PipeExec, self).__init__()
        config = self.import_config(config_file)
        self.pipe_name = config.pipe_name
        self.set_mail_params(**config.mail)

    def set_mail_params(self, mail_server=None, mail_port=None, mail_user=None, mail_password=None,
                        mail_use_tls=True, mail_default_receiver=None):
        self.mail_server = mail_server
        self.mail_port = mail_port
        self.mail_user = mail_user
        self.mail_password = mail_password
        self.mail_use_tls = mail_use_tls
        self.mail_default_receiver = mail_default_receiver

    def get_subject(self, subject=""):
        l_subject = []
        if self.mail_subject:
            l_subject.append(f'[{self.pipe_name}]')
        if subject:
            l_subject.append(subject)
        return ' - '.join(l_subject)

    def mail_is_configured(self):
        return self.mail_server and self.mail_port and self.mail_user and self.mail_password

    @staticmethod
    def import_config(config_file):
        try:
            return import_config(config_file, os.path.dirname(os.path.abspath(__file__)))
        except ConfigNotFoundError:
            return Config(dict(mail=dict(), pipe_name=None))

    # Actions
    def send_mail(self, message, receiver_email, subject=None, cc=None, bcc=None, subtype='md', attachments=None):
        if self.mail_is_configured():
            with Email(self.mail_server, self.mail_port, self.mail_user, self.mail_password, self.mail_use_tls) as email:
                email.send_message(message, receiver_email, self.get_subject(subject), cc=cc, bcc=bcc,
                                   subtype=subtype, attachments=attachments)

    def notify(self, message, title=None, app_icon="", timeout=10):
        notification.notify(
            title=self.get_subject(title),
            message=message,
            app_icon=app_icon,
            timeout=timeout,  # seconds
        )

    # Handler
    def handler(self, action: ActionBase, exception, *args, **kwargs):
        if self.mail_default_receiver and self.mail_is_configured():
            tb = traceback.format_exc()
            message = "##" + '\n\n'.join(map(lambda x: f'<span style="color: red;">{x}</span>', tb.split('\n')))
            subject = f'Error: {exception}'
            self.send_mail(message, self.mail_default_receiver, subject)
        return super(PipeExec, self).handler(action, exception, *args, **kwargs)
