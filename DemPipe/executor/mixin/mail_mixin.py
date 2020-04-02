from Dmail import Email
from configDmanager import Config

from DemPipe.executor.mixin import ConfigMixin


class EmailMixin(ConfigMixin):
    def __init__(self, config_file=None):
        self.mail_server = None
        self.mail_port = None
        self.mail_user = None
        self.mail_password = None
        self.mail_use_tls = True
        self.mail_default_receiver = None
        super(EmailMixin, self).__init__(config_file)

    def load_config(self, config):
        super(EmailMixin, self).load_config(config)
        self.set_mail_params(**config.mail)

    def set_default_config(self, config):
        super(EmailMixin, self).set_default_config(config)
        config.mail = Config(dict())

    def set_mail_params(self, mail_server=None, mail_port=None, mail_user=None, mail_password=None,
                        mail_use_tls=True, mail_default_receiver=None):
        self.mail_server = mail_server
        self.mail_port = mail_port
        self.mail_user = mail_user
        self.mail_password = mail_password
        self.mail_use_tls = mail_use_tls
        self.mail_default_receiver = mail_default_receiver

    def mail_is_configured(self):
        return self.mail_server and self.mail_port and self.mail_user and self.mail_password

    # Actions
    def send_mail(self, message, receiver_email, subject=None, cc=None, bcc=None, subtype=None, attachments=None):
        if self.mail_is_configured():
            with Email(self.mail_server, self.mail_port, self.mail_user, self.mail_password, self.mail_use_tls) as email:
                email.send(message, receiver_email, self.get_title(subject), cc=cc, bcc=bcc, subtype=subtype,
                           attachments=attachments)
