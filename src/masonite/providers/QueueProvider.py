from ..drivers.queue import DatabaseDriver, AsyncDriver, AMQPDriver
from ..queues import Queue
from ..utils.structures import load


class QueueProvider:
    def __init__(self, application):
        self.application = application

    def register(self):
        queue = Queue(self.application).set_configuration(
            load(self.application.make("config.queue")).DRIVERS
        )

        queue.add_driver("database", DatabaseDriver(self.application))
        queue.add_driver("async", AsyncDriver(self.application))
        queue.add_driver("amqp", AMQPDriver(self.application))
        self.application.bind("queue", queue)

    def boot(self):
        pass
