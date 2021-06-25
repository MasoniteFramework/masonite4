from tests import TestCase
from src.masonite.facades import Mail


class TestFacades(TestCase):
    def test_mail_facade(self):
        self.assertIsNone(Mail.get_config_options("mailgun")['domain'])

