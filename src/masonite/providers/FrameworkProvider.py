from ..foundation import response_handler
from ..request import Request
from ..response import Response


class FrameworkProvider:
    def __init__(self, application):
        self.application = application

    def register(self):
        pass

    def boot(self):
        print("framework boot")
        self.application.bind("request", Request(self.application.make("environ")))
        self.application.bind("response", Response(self.application))
