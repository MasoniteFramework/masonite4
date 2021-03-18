from tests import TestCase
import responses
from src.masonite.notification import Notification, Notifiable, SlackMessage

from masoniteorm.models import Model

# fake webhook for tests
webhook_url = "https://hooks.slack.com/services/X/Y/Z"
webhook_url_2 = "https://hooks.slack.com/services/A/B/C"


class User(Model, Notifiable):
    """User Model"""

    __fillable__ = ["name", "email", "password", "phone"]

    def route_notification_for_slack(self):
        return "#general"
        return ["#general", "#news"]
        return webhook_url
        return [webhook_url, webhook_url_2]


# class WelcomeUserNotification(Notification):
#     def to_slack(self, notifiable):
#         return Sms().to(notifiable.phone).text("Welcome !").from_("123456")

#     def via(self, notifiable):
#         return ["slack"]


class WelcomeNotification(Notification):
    def to_slack(self, notifiable):
        return SlackMessage().text("Welcome !").from_("test-bot")

    def via(self, notifiable):
        return ["slack"]


class OtherNotification(Notification):
    def to_slack(self, notifiable):
        return (
            SlackMessage()
            .channel(["#general", "#news"])
            .text("Welcome !")
            .from_("test-bot")
        )

    def via(self, notifiable):
        return ["slack"]


class WebhookNotification(Notification):
    def to_slack(self, notifiable):
        return SlackMessage().webhook(webhook_url).text("Welcome !").from_("test-bot")

    def via(self, notifiable):
        return ["slack"]


class TestSlackDriver(TestCase):
    def setUp(self):
        super().setUp()
        self.notification = self.application.make("notification")

    @responses.activate
    def test_sending_to_anonymous_via_webhook(self):
        responses.add(responses.POST, webhook_url, body=b"ok")
        self.notification.route("slack", webhook_url).notify(WelcomeNotification())
        self.assertTrue(responses.assert_call_count(webhook_url, 1))

    # def test_send_to_anonymous(self):
    # with patch("vonage.sms.Sms") as MockSmsClass:
    #     MockSmsClass.return_value.send_message.return_value = (
    #         VonageAPIMock().send_success()
    #     )
    # self.notification.route("slack", "#general").send(WelcomeNotification())

    # def test_send_to_notifiable(self):
    #     with patch("vonage.sms.Sms") as MockSmsClass:
    #         MockSmsClass.return_value.send_message.return_value = (
    #             VonageAPIMock().send_success()
    #         )
    #         user = User.find(1)
    #         user.notify(WelcomeUserNotification())