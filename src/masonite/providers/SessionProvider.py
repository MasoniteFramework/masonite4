from .Provider import Provider
from ..sessions import Session
from ..drivers.session import CookieDriver
from ..utils.structures import config, load


class SessionProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        session = Session(self.application).set_configuration(
            load(self.application.make("config.session")).DRIVERS
        )
        session.add_driver("cookie", CookieDriver(self.application))
        self.application.bind("session", session)

    def boot(self):
        self.application.make("request").session = self.application.make("session")
