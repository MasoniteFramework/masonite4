from tests import TestCase


class TestFacades(TestCase):
    def test_mail_facade(self):
        assert self.application.make("mail") == Mail
        assert self.application.make("storage") == Storage

        Mail.get_config_options("mailgun")
