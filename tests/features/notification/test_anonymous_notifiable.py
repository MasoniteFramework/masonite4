from tests import TestCase

from src.masonite.notification import Notification, AnonymousNotifiable


class WelcomeNotification(Notification):
    def to_mail(self, notifiable):
        pass

    def via(self, notifiable):
        return ["mail"]


class TestAnonymousNotifiable(TestCase):
    def test_one_routing(self):
        notifiable = AnonymousNotifiable().route("mail", "user@example.com")
        self.assertDictEqual({"mail": "user@example.com"}, notifiable._routes)

    def test_multiple_routing(self):
        notifiable = (
            AnonymousNotifiable()
            .route("mail", "user@example.com")
            .route("slack", "#general")
        )
        self.assertDictEqual(
            {"mail": "user@example.com", "slack": "#general"}, notifiable._routes
        )

    def test_that_sending_with_unexisting_driver_raise_exception(self):
        with self.assertRaises(ValueError) as err:
            AnonymousNotifiable().route_notification_for("custom_sms", "+337232323232")
        self.assertEqual(
            "Routing has not been defined for the channel custom_sms",
            str(err.exception),
        )

    def test_can_override_dry_when_sending(self):
        AnonymousNotifiable().route("mail", "user@example.com").send(
            WelcomeNotification(), dry=True
        )
        # TODO: assert it

    def test_can_override_fail_silently_when_sending(self):
        AnonymousNotifiable().route("mail", "user@example.com").send(
            WelcomeNotification(), fail_silently=True
        )
        # TODO: assert it
