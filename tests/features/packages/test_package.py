from tests import TestCase
from src.masonite.utils.structures import load


class TestPackageProvider(TestCase):
    def setUp(self):
        super().setUp()

    def test_can_access_registered_config(self):
        path = self.application.make("config.package")
        self.assertTrue(path.endswith("tests/integrations/testpackage/params.py"))
        # data = load(self.application.make("config.package"))
        # import pdb

        # pdb.set_trace()

    def test_can_call_publish_command_for_this_package(self):
        self.craft("publish", "test-package")
