"""Vonage driver Class."""
from ....exceptions import NotificationException
from ..BaseDriver import BaseDriver
from .Sms import Sms


class VonageDriver(BaseDriver):
    def __init__(self, application):
        self.app = application
        self.options = {}

    def set_options(self, options):
        self.options = options
        return self

    def build(self, notifiable, notification):
        """Prepare SMS and list of recipients."""
        data = self.get_data("vonage", notifiable, notification)
        recipients = self.get_recipients("vonage", notifiable, notification)
        return data, recipients

    def get_sms_client(self):
        try:
            import vonage
            from vonage.sms import Sms
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'vonage' library. Run 'pip install vonage' to fix this."
            )
        client = vonage.Client(
            key=self.options.get("key"), secret=self.options.get("secret")
        )
        return Sms(client)

    def send(self, notifiable, notification):
        """Used to send the SMS."""
        data, recipients = self.build(notifiable, notification)
        responses = []
        client = self.get_sms_client()

        for recipient in recipients:
            payload = self.build_payload(data, recipient)
            response = client.send_message(payload)
            self._handle_errors(response)
            responses.append(response)
        return responses

    def queue(self, notifiable, notification):
        """Used to queue the SMS notification to be send."""
        data, recipients, sms = self._prepare_sms(notifiable, notification)
        for recipient in recipients:
            payload = self.build_payload(data, recipient)
            self.application.make("queue").push(sms.send_message, args=(payload,))

    def get_recipients(self, notifiable, notification):
        """Get recipients which can be defined through notifiable route method.
        It can be one or a list of phone numbers.
            return phone
            return [phone1, phone2]
        """
        recipients = notifiable.route_notification_for("vonage", notification)
        # multiple recipients
        if isinstance(recipients, list):
            _recipients = []
            for recipient in recipients:
                _recipients.append(recipient)
        else:
            _recipients = [recipients]
        return _recipients

    def build_payload(self, data, recipient):
        """Build SMS payload sent to Vonage API."""

        if isinstance(data, str):
            data = Sms(data)

        # define send_from from config if not set
        if not data._from:
            data = data.send_from(self.options.get("sms_from"))
        payload = {**data.as_dict(), "to": recipient}
        self._validate_payload(payload)
        return payload

    def _validate_payload(self, payload):
        """Validate SMS payload before sending by checking that from et to
        are correctly set."""
        if not payload.get("from", None):
            raise NotificationException("from must be specified.")
        if not payload.get("to", None):
            raise NotificationException("to must be specified.")

    def _handle_errors(self, response):
        """Handle errors of Vonage API. Raises VonageAPIError if request does
        not succeed.

        An error message is structured as follows:
        {'message-count': '1', 'messages': [{'status': '2', 'error-text': 'Missing api_key'}]}
        As a success message can be structured as follows:
        {'message-count': '1', 'messages': [{'to': '3365231278', 'message-id': '140000012BD37332', 'status': '0',
        'remaining-balance': '1.87440000', 'message-price': '0.06280000', 'network': '20810'}]}

        More informations on status code errors: https://developer.nexmo.com/api-errors/sms

        """
        for message in response.get("messages", []):
            status = message["status"]
            if status != "0":
                raise NotificationException(
                    "Vonage Code [{0}]: {1}. Please refer to API documentation for more details.".format(
                        status, message["error-text"]
                    )
                )
