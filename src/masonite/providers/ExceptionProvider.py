from .Provider import Provider
from exceptionite.errors import Handler, StackOverflowIntegration, SolutionsIntegration
from ..exceptions import ExceptionHandler

class ExceptionProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        handler = ExceptionHandler(self.application)
        self.application.bind("exception_handler", handler)

    def boot(self):
        pass
