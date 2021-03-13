from tests import TestCase

from src.masonite.notification import Notification


class WelcomeNotification(Notification):
    def to_mail(self, notifiable):
        return ""

    def via(self, notifiable):
        return ["mail"]


class TestNotification(TestCase):
    def test_should_send(self):
        notification = WelcomeNotification()
        self.assertTrue(notification.should_send)
        notification.dry()
        self.assertFalse(notification.should_send)

    def test_ignore_errors(self):
        notification = WelcomeNotification()
        self.assertFalse(notification.ignore_errors)
        notification.fail_silently()
        self.assertTrue(notification.ignore_errors)

    def test_notification_type(self):
        self.assertEqual("WelcomeNotification", WelcomeNotification().type())
