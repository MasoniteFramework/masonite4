from ...providers import Provider
from ..Event import Event
from ...utils.structures import config, load


class EventProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        event = Event(self.application)
        self.application.bind("event", event)

    def boot(self):
        pass
