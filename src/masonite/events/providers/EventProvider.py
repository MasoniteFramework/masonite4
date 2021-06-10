from ...providers import Provider
from ..Event import Event
from ..commands.MakeListenerCommand import MakeListenerCommand


class EventProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        event = Event(self.application)
        self.application.make("commands").add(MakeListenerCommand(self.application))
        self.application.bind("event", event)

    def boot(self):
        pass
