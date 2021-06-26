from tests import TestCase
from src.masonite.facades import Hash


class TestHashers(TestCase):
    def test_bcrypt_hasher(self):
        hashed = Hash.make("masonite")
        assert hashed != "masonite"
        assert Hash.check("masonite", hashed)

    def test_argon2_hasher(self):
        hashed = Hash.make("masonite", driver="argon2")
        assert hashed != "masonite"
        assert Hash.check("masonite", hashed, driver="argon2")
