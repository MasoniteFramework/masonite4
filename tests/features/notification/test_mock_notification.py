from tests import TestCase

from src.masonite.notification import Notification, Notifiable
from src.masonite.mail import Mailable
from masoniteorm.models import Model


class User(Model, Notifiable):
    """User Model"""

    __fillable__ = ["name", "email", "password"]


class WelcomeNotification(Notification):
    def to_mail(self, notifiable):
        return (
            Mailable()
            .subject("Masonite 4")
            .from_("joe@masoniteproject.com")
            .text("Hello from Masonite!")
        )

    def via(self, notifiable):
        return ["mail"]


class OtherNotification(Notification):
    def to_mail(self, notifiable):
        return (
            Mailable()
            .subject("Other")
            .from_("sam@masoniteproject.com")
            .text("Hello again!")
        )

    def via(self, notifiable):
        return ["mail"]


class TestMockNotification(TestCase):
    def setUp(self):
        super().setUp()
        self.fake("notification")

    def tearDown(self):
        super().tearDown()
        self.restore("notification")

    def test_assert_nothing_sent(self):
        notification = self.application.make("notification")
        notification.assertNothingSent()

    def test_assert_count(self):
        notification = self.application.make("notification")
        notification.assertCount(0)
        notification.route("mail", "test@mail.com").send(WelcomeNotification())
        notification.assertCount(1)
        notification.route("mail", "test2@mail.com").send(WelcomeNotification())
        notification.assertCount(2)

    def test_reset_count(self):
        notification = self.application.make("notification")
        notification.assertNothingSent()
        notification.route("mail", "test@mail.com").send(WelcomeNotification())
        notification.resetCount()
        notification.assertNothingSent()

    def test_assert_sent_to_with_anonymous(self):
        notification = self.application.make("notification")
        notification.route("mail", "test@mail.com").send(WelcomeNotification())
        notification.assertSentTo("test@mail.com", WelcomeNotification)

        notification.route("vonage", "123456").route("slack", "#general").send(
            WelcomeNotification()
        )
        notification.assertSentTo("123456", WelcomeNotification)
        notification.assertSentTo("#general", WelcomeNotification)

    def test_assert_not_sent_to(self):
        notification = self.application.make("notification")
        notification.resetCount()
        notification.assertNotSentTo("test@mail.com", WelcomeNotification)
        notification.route("vonage", "123456").send(OtherNotification())
        notification.assertNotSentTo("123456", WelcomeNotification)
        notification.assertNotSentTo("test@mail.com", OtherNotification)

    def test_assert_sent_to_with_notifiable(self):
        notification = self.application.make("notification")
        user = User.find(1)
        user.notify(WelcomeNotification())
        notification.assertSentTo(user, WelcomeNotification)
        user.notify(OtherNotification())
        notification.assertSentTo(user, OtherNotification)
        notification.assertCount(2)

    def test_assert_sent_to_with_count(self):
        notification = self.application.make("notification")
        user = User.find(1)
        user.notify(WelcomeNotification())
        user.notify(WelcomeNotification())
        notification.assertSentTo(user, WelcomeNotification, 2)

        user.notify(OtherNotification())
        user.notify(OtherNotification())
        with self.assertRaises(AssertionError):
            notification.assertSentTo(user, OtherNotification, 1)
