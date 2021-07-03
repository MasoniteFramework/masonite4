from ..hashing import Hash
from ..hashing.drivers import BcryptHasher, Argon2Hasher
from .Provider import Provider
from ..utils.structures import load


class HashServiceProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        hashing = Hash(self.application).set_configuration(
            load(self.application.make("config.application")).HASHING
        )
        hashing.add_driver("bcrypt", BcryptHasher())
        hashing.add_driver("argon2", Argon2Hasher())
        self.application.bind("hash", hashing)

    def boot(self):
        pass
