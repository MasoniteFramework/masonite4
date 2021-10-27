from .Provider import Provider
from ..sessions import Session
from ..drivers.session import CookieDriver
from ..utils.structures import load
from ..configuration import config


class SessionProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        session = Session(self.application).set_configuration(config("session.drivers"))
        session.add_driver("cookie", CookieDriver(self.application))
        self.application.bind("session", session)
        self.application.make("view").share({"old": self.old})

    def boot(self):
        pass

    def old(self, key):
        return self.application.make("session").get(key) or ""
