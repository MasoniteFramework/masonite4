"""Slack driver Class"""
import requests
from masonite.app import App
from masonite.helpers import config
from masonite.managers.QueueManager import Queue

from ..exceptions import (
    SlackChannelNotFound,
    SlackInvalidMessage,
    SlackInvalidWorkspace,
    SlackChannelArchived,
    SlackInvalidWebhook,
    SlackAPIError,
)
from .BaseDriver import BaseDriver


class SlackDriver(BaseDriver):

    app = None
    WEBHOOK_MODE = 1
    API_MODE = 2
    sending_mode = WEBHOOK_MODE

    def __init__(self, application):
        self.application = application
        self.options = {}
        # TODO
        self._debug = False
        self._token = config("notifications.slack.token", None)

    def send(self, notifiable, notification):
        """Used to send the notification to slack."""
        method, method_args = self._prepare_slack_message(notifiable, notification)
        return method(*method_args)

    def queue(self, notifiable, notification):
        """Used to queue the notification to be sent to slack."""
        method, method_args = self._prepare_slack_message(notifiable, notification)
        return self.app.make(Queue).push(method, args=method_args)

    def _prepare_slack_message(self, notifiable, notification):
        """Prepare slack message to be sent."""
        data = self.get_data("slack", notifiable, notification)
        recipients = self.get_recipients(notifiable, notification)
        if self.sending_mode == self.WEBHOOK_MODE:
            send_method = self.send_via_webhook
        else:
            send_method = self.send_via_api
        return send_method, (data, recipients)

    def get_recipients(self, notifiable, notification):
        """Get recipients which can be defined through notifiable route method.
        For Slack it can be:
            - an incoming webhook (or a list of incoming webhooks) that you defined in your app
            return webhook_url
            return [webhook_url_1, webhook_url_2]
            - a channel name or ID (it will use Slack API and requires a Slack token
            for accessing your workspace)
            return "{channel_name or channel_id}"
            return [channel_name_1, channel_name_2]
        You cannot mix both.
        """
        recipients = notifiable.route_notification_for("slack", notification)
        if isinstance(recipients, list):
            _modes = []
            for recipient in recipients:
                _modes.append(self._check_recipient_type(recipient))
            if self.API_MODE in _modes and self.WEBHOOK_MODE in _modes:
                raise ValueError(
                    "NotificationSlackDriver: sending mode cannot be mixed."
                )
            mode = _modes[0]
        else:
            mode = self._check_recipient_type(recipients)
            recipients = [recipients]

        self.sending_mode = mode
        return recipients

    def _check_recipient_type(self, recipient):
        if recipient.startswith("https://hooks.slack.com"):
            return self.WEBHOOK_MODE
        else:
            return self.API_MODE

    def send_via_webhook(self, payload, webhook_urls):
        data = payload.as_dict()
        if self._debug:
            print(data)
        for webhook_url in webhook_urls:
            response = requests.post(
                webhook_url, data=data, headers={"Content-Type": "application/json"}
            )
            if response.status_code != 200:
                self._handle_webhook_error(response, data)

    def send_via_api(self, payload, channels):
        """Send Slack notification with Slack Web API as documented
        here https://api.slack.com/methods/chat.postMessage"""
        for channel in channels:
            # if notification._as_snippet:
            #     requests.post('https://slack.com/api/files.upload', {
            #         'token': notification._token,
            #         'channel': channel,
            #         'content': notification._text,
            #         'filename': notification._snippet_name,
            #         'filetype': notification._type,
            #         'initial_comment': notification._initial_comment,
            #         'title': notification._title,
            #     })
            # else:
            # use notification defined token else globally configured token
            token = payload._token or self._token
            channel = self._get_channel_id(channel, token)
            payload = {
                **payload.as_dict(),
                # mandatory
                "token": token,
                "channel": channel,
            }
            if self._debug:
                print(payload)
            self._call_slack_api("https://slack.com/api/chat.postMessage", payload)

    def _call_slack_api(self, url, payload):
        response = requests.post(url, payload)
        data = response.json()
        if not data["ok"]:
            self._raise_related_error(data["error"], payload)
        else:
            return data

    def _handle_webhook_error(self, response, payload):
        self._raise_related_error(response.text, payload)

    def _raise_related_error(self, error_key, payload):
        if error_key == "invalid_payload":
            raise SlackInvalidMessage(
                "The message is malformed: perhaps the JSON is structured incorrectly, or the message text is not properly escaped."
            )
        elif error_key == "invalid_auth":
            raise SlackAPIError(
                "Some aspect of authentication cannot be validated. Either the provided token is invalid or the request originates from an IP address disallowed from making the request."
            )
        elif error_key == "too_many_attachments":
            raise SlackInvalidMessage(
                "Too many attachments: the message can have a maximum of 100 attachments associated with it."
            )
        elif error_key == "channel_not_found":
            raise SlackChannelNotFound(
                "The user or channel being addressed either do not exist or is invalid: {}".format(
                    payload["channel"]
                )
            )
        elif error_key == "channel_is_archived":
            raise SlackChannelArchived(
                "The channel being addressed has been archived and is no longer accepting new messages: {}".format(
                    payload["channel"]
                )
            )
        elif error_key in [
            "action_prohibited",
            "posting_to_general_channel_denied",
        ]:
            raise SlackAPIError(
                "You don't have the permission to post to this channel right now: {}".format(
                    payload["channel"]
                )
            )
        elif error_key in ["no_service", "no_service_id"]:
            raise SlackInvalidWebhook(
                "The provided incoming webhook is either disabled, removed or invalid."
            )
        elif error_key in ["no_team", "team_disabled"]:
            raise SlackInvalidWorkspace(
                "The Slack workspace is no longer active or is missing or invalid."
            )
        else:
            raise SlackAPIError("{}. Check Slack API docs.".format(error_key))

    def _get_channel_id(self, name, token):
        """"Returns Slack channel's ID from given channel."""
        if "#" in name:
            return self._find_channel(name, token)
        else:
            return name

    def _find_channel(self, name, token):
        """Calls the Slack API to find the channel name. This is so we do not have to specify the channel ID's.
        Slack requires channel ID's to be used.

        Arguments:
            name {string} -- The channel name to find.

        Raises:
            SlackChannelNotFound -- Thrown if the channel name is not found.

        Returns:
            self
        """
        response = self._call_slack_api(
            "https://slack.com/api/conversations.list", {"token": token}
        )
        for channel in response["channels"]:
            if channel["name"] == name.split("#")[1]:
                return channel["id"]

        raise SlackChannelNotFound(
            "The user or channel being addressed either do not exist or is invalid: {}".format(
                name
            )
        )
