from .Provider import Provider
from exceptionite.errors import Handler, StackOverflowIntegration, SolutionsIntegration
from ..exceptions import ExceptionHandler, DumpExceptionHandler, DD
import builtins


class ExceptionProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        handler = ExceptionHandler(self.application)
        builtins.dd = DD(self.application).dump
        self.application.bind("exception_handler", handler)
        self.application.bind(
            "DumpExceptionHandler", DumpExceptionHandler(self.application)
        )

    def boot(self):
        pass
