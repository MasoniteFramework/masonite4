from .Provider import Provider
from ..cache import Cache
from ..cache.drivers import FileDriver
from ..utils.structures import load


class CacheProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        cache = Cache(self.application).set_configuration(
            load(self.application.make("config.cache")).STORES
        )
        cache.add_driver("file", FileDriver(self.application))
        self.application.bind("cache", cache)

    def boot(self):
        pass
