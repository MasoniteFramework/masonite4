from ...providers.Provider import Provider

from ...commands import MakeModelCommand


class InternalORMProvider(Provider):
    """Allow to tweak official ORMPRovider when used inside Masonite."""

    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.make("commands").swap(MakeModelCommand(self.application))
