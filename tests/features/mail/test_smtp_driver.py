from tests import TestCase
from src.masonite.drivers.mail.Recipient import Recipient
from unittest.mock import MagicMock
import os
from src.masonite.mail import Mailable


class Welcome(Mailable):
    def build(self):
        return (
            self.to("idmann509@gmail.com")
            .subject("Masonite 4")
            .from_("joe@masoniteproject.com")
            .text("Hello from Masonite!")
            .html("<h1>Hello from Masonite!</h1>")
        )


class TestSMTPDriver(TestCase):
    def test_send_mailable(self):
        if os.getenv("RUN_MAIL") == True:
            self.application.make("mail").mailable(Welcome())
