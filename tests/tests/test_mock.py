from tests import TestCase
from src.masonite.mail import Mail, MockMail


class CustomMockMail:
    def __init__(self, application):
        self.application = application


class TestMocking(TestCase):
    def test_fake_service(self):
        mocked_mail = self.fake("mail")

        assert isinstance(self.application.make("mail"), MockMail)
        assert isinstance(mocked_mail, MockMail)

        self.restore("mail")

        assert isinstance(self.application.make("mail"), Mail)

    def test_fake_with_custom_mock(self):
        mocked_mail = self.fake("mail", CustomMockMail)

        assert isinstance(self.application.make("mail"), CustomMockMail)
        assert isinstance(mocked_mail, CustomMockMail)

        self.restore("mail")
        assert isinstance(self.application.make("mail"), Mail)
