from tests import TestCase
from src.masonite.middleware import EncryptCookies


class TestEncryptCookiesMiddleware(TestCase):
    def test_encrypts_cookies(self):
        request = self.make_request(
            {"HTTP_COOKIE": f"test={self.application.make('sign').sign('value')}"}
        )
        EncryptCookies().before(request, None)
        self.assertEqual(request.cookie("test"), "value")

        EncryptCookies().after(request, None)
        self.assertNotEqual(request.cookie("test"), "value")
