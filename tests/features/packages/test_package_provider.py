from src.masonite.configuration import config

from tests import TestCase


class TestPackageProvider(TestCase):
    def setUp(self):
        super().setUp()

    def test_config_is_loaded(self):
        self.assertEqual(config("test_package.param_2"), 1)

    def test_config_is_merged(self):
        self.assertEqual(config("test_package.param_1"), 0)

    # def test_package_config_can_be_published(self):
    #     pp = self.application.providers[-1]
    #     import pdb

    #     pdb.set_trace()

    def test_views_are_registered(self):
        self.application.make("view").exists("package")
        self.application.make("view").exists("package_base")
        self.application.make("view").exists("admin.settings")

    def test_commands_are_registered(self):
        self.craft("test_package:command1").assertSuccess()
        self.craft("test_package:command2").assertSuccess()

    # def test_routes_are_registered(self):
    #     self.get("package/test")
