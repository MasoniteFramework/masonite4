from tests import TestCase
from src.masonite.facades import Config
from src.masonite.configuration import config


class TestConfiguration(TestCase):
    def test_config_is_loaded(self):
        self.assertGreater(len(Config._config.keys()), 0)

    def test_base_configuration_files_can_be_accessed(self):
        self.assertIsNotNone("config.application")
        self.assertIsNotNone("config.auth")
        self.assertIsNotNone("config.broadcast")
        self.assertIsNotNone("config.cache")
        self.assertIsNotNone("config.database")
        self.assertIsNotNone("config.filesystem")
        self.assertIsNotNone("config.mail")
        self.assertIsNotNone("config.notification")
        self.assertIsNotNone("config.providers")
        self.assertIsNotNone("config.queue")
        self.assertIsNotNone("config.session")

    def test_config_helper(self):
        self.assertEqual(config("auth.guards.default"), "web")

    def test_config_facade(self):
        self.assertEqual(Config.get("auth.guards.default"), "web")

    def test_config_use_default_if_not_exist(self):
        self.assertEqual(config("some.app"), None)
        self.assertEqual(config("some.app", 0), 0)

    def test_config_set_value(self):
        original_value = config("cache.stores.redis.port")
        Config.set("cache.stores.redis.port", 1000)
        self.assertNotEqual(Config.get("cache.stores.redis.port"), original_value)
        self.assertEqual(Config.get("cache.stores.redis.port"), 1000)
        # reset to original value
        Config.set("cache.stores.redis.port", original_value)
