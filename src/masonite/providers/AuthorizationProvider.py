from ..authorization import Authorization, Gate
from .Provider import Provider


class AuthorizationProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        # from ..facades import Request

        authorization = Authorization(self.application)
        self.application.bind("authorization", authorization)
        self.application.bind("gate", Gate(self.application))

    def boot(self):
        pass
