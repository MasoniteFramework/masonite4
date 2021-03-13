from masonite.queues import Queueable


class SayHello(Queueable):
    def handle(self):
        pass
