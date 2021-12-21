from masoniteorm.providers import ORMProvider

from ...commands import MakeModelCommand


class InternalORMProvider(ORMProvider):
    """Allow to tweak official ORMPRovider when used inside Masonite."""

    def __init__(self, application):
        self.application = application

    def register(self):
        super().register(self)
        # replace some commands to be used with Masonite
        self.application.make("commands").swap(MakeModelCommand(self.application))
