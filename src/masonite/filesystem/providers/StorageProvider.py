from ...providers import Provider
from ..Storage import Storage
from ...utils.structures import load
from ..drivers import LocalDriver


class StorageProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        storage = Storage(self.application).set_configuration(
            load(self.application.make("config.filesystem")).DISKS
        )

        storage.add_driver("file", LocalDriver(self.application))
        self.application.bind("storage", storage)

    def boot(self):
        pass
