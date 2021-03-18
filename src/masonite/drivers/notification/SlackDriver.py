"""Slack notification driver"""
import requests

from ...exceptions import NotificationException
from .BaseDriver import BaseDriver


class SlackDriver(BaseDriver):

    WEBHOOK_MODE = 1
    API_MODE = 2
    send_url = "https://slack.com/api/chat.postMessage"
    channel_url = "https://slack.com/api/conversations.list"

    def __init__(self, application):
        self.application = application
        self.options = {}
        self.mode = self.WEBHOOK_MODE

    def set_options(self, options):
        self.options = options
        return self

    def send(self, notifiable, notification):
        """Used to send the notification to slack."""
        self.mode = self.get_sending_mode()
        slack_message = self.build(notifiable, notification)
        if self.mode == self.WEBHOOK_MODE:
            self.send_via_webhook(slack_message)
        else:
            self.send_via_api(slack_message)

    # def queue(self, notifiable, notification):
    # TODO
    #     """Used to queue the notification to be sent to slack."""
    #     method, payload = self.prepare(notifiable, notification)
    #     return self.application.make("queue").push(method, args=payload)

    def build(self, notifiable, notification):
        """Build Slack message payload sent to Slack API or through Slack webhook."""
        slack_message = self.get_data("slack", notifiable, notification)
        if self.mode == self.WEBHOOK_MODE and not slack_message._webhook:
            webhooks = self.get_recipients(notifiable)
            slack_message = slack_message.webhook(webhooks)
        elif self.mode == self.API_MODE:
            if not slack_message._channel:
                channels = self.get_recipients(notifiable)
                slack_message = slack_message.channel(channels)
            if not slack_message._token:
                slack_message = slack_message.token(self.options.get("token"))
        return slack_message.build().get_options()

    def get_recipients(self, notifiable):
        recipients = notifiable.route_notification_for("slack")
        if not isinstance(recipients, (list, tuple)):
            recipients = [recipients]
        return recipients

    def get_sending_mode(self):
        # if recipient.startswith("https://hooks.slack.com"):
        #     return self.WEBHOOK_MODE
        # else:
        #     return self.API_MODE
        mode = self.options.get("mode", "webhook")
        if mode == "webhook":
            return self.WEBHOOK_MODE
        else:
            return self.API_MODE

    def send_via_webhook(self, slack_message):
        for webhook_url in slack_message._webhook:
            response = requests.post(
                webhook_url,
                data=slack_message,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code != 200:
                raise NotificationException(
                    "{}. Check Slack webhooks docs.".format(response.text)
                )

    def send_via_api(self, slack_message):
        """Send Slack notification with Slack Web API as documented
        here https://api.slack.com/methods/chat.postMessage"""
        # TODO: how to get channels

        for channel in slack_message._channel:
            channel = self.convert_channel(channel, slack_message._token)
            slack_message.to(channel)
            response = requests.post(self.send_url, slack_message).json()
            if not response["ok"]:
                raise NotificationException(
                    "{}. Check Slack API docs.".format(response["error"])
                )
            else:
                return response

    def convert_channel(self, name, token):
        """Calls the Slack API to find the channel ID if not already a channel ID.

        Arguments:
            name {string} -- The channel name to find.
        """
        if "#" not in name:
            return name
        response = requests.post(self.channel_url, {"token": token}).json()
        for channel in response["channels"]:
            if channel["name"] == name.split("#")[1]:
                return channel["id"]

        raise NotificationException(
            f"The user or channel being addressed either do not exist or is invalid: {name}"
        )
