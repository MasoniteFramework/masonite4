from ..foundation import response_handler
from ..request import Request
from ..response import Response
from ..authentication import Auth
from ..authentication.guards import WebGuard
from ..utils.structures import load
from .Provider import Provider


class AuthenticationProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        auth = Auth(self.application).set_configuration(
            load(self.application.make("config.auth")).GUARDS
        )

        auth.add_guard("web", WebGuard(self.application))

        self.application.bind("auth", auth)

    def boot(self):
        pass
