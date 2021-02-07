from ..foundation import response_handler
from ..request import Request
from ..response import Response
from .Provider import Provider
from ..mail import Mail
from ..drivers.mail import SMTPDriver, MailgunDriver, TerminalDriver
from ..utils.structures import config, load


class MailProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        mail = Mail(self.application).set_configuration(
            load(self.application.make("config.mail")).DRIVERS
        )
        mail.add_driver("smtp", SMTPDriver(self.application))
        mail.add_driver("mailgun", MailgunDriver(self.application))
        mail.add_driver("terminal", TerminalDriver(self.application))
        self.application.bind("mail", mail)

    def boot(self):
        pass
