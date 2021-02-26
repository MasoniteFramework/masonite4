from ...providers import Provider
from ..Broadcast import Broadcast
from ..drivers import PusherDriver
from ...utils.structures import load


class BroadcastProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        broadcast = Broadcast(self.application).set_configuration(
            load(self.application.make("config.broadcast")).BROADCASTS
        )

        broadcast.add_driver("pusher", PusherDriver(self.application))

        self.application.bind("broadcast", broadcast)

    def boot(self):
        pass
