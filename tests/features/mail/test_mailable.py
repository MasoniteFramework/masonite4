from tests import TestCase
from src.masonite.mail import Mailable
from src.masonite.drivers.mail.Recipient import Recipient
import os


class Welcome(Mailable):
    def build(self):
        return (
            self.to("idmann509@gmail.com")
            .subject("Masonite 4")
            .from_("joe@masoniteproject.com")
            .text("Hello from Masonite!")
            .html("<h1>Hello from Masonite!</h1>")
        )


class TestMailable(TestCase):
    def setUp(self):
        super().setUp()
        self.application.make("mail")

    def test_build_mail(self):
        mailable = Welcome().build().get_options()
        self.assertEqual(mailable.get("to"), "idmann509@gmail.com")
        self.assertEqual(mailable.get("from"), "joe@masoniteproject.com")
        self.assertEqual(mailable.get("subject"), "Masonite 4")
        self.assertEqual(mailable.get("text_content"), "Hello from Masonite!")
        self.assertEqual(mailable.get("html_content"), "<h1>Hello from Masonite!</h1>")
        self.assertEqual(mailable.get("reply_to"), "")

    def test_recipient(self):
        to = Recipient("idmann509@gmail.com, joe@masoniteproject.com")
        self.assertEqual(
            to.header(), "<idmann509@gmail.com>, <joe@masoniteproject.com>"
        )
        to = Recipient("Joseph Mancuso <idmann509@gmail.com>, joe@masoniteproject.com")
        self.assertEqual(
            to.header(),
            "Joseph Mancuso <idmann509@gmail.com>, <joe@masoniteproject.com>",
        )
