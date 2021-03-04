from ...providers import Provider
from ..guards import APIGuard


class APIProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.make("auth").add_guard("api", APIGuard(self.application))

    def boot(self):
        pass
