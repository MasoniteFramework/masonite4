from ..foundation import response_handler
from ..request import Request
from ..response import Response


class AuthenticationProvider:
    def __init__(self, application):
        self.application = application

    def register(self):
        # Register authentication class
        pass

    def boot(self):
        pass
