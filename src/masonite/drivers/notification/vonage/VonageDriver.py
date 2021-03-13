"""Vonage notification driver."""
from ....exceptions import NotificationException
from ..BaseDriver import BaseDriver


class VonageDriver(BaseDriver):
    def __init__(self, application):
        self.app = application
        self.options = {}

    def set_options(self, options):
        self.options = options
        return self

    def build(self, notifiable, notification):
        """Build SMS payload sent to Vonage API."""
        sms = self.get_data("vonage", notifiable, notification)
        if not sms._from:
            sms = sms.from_(self.options.get("sms_from"))
        if not sms._to:
            recipients = notifiable.route_notification_for("vonage")
            sms = sms.to(recipients)
        return sms.build().get_options()

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
        sms = self.build(notifiable, notification)
        client = self.get_sms_client()
        # TODO: here if multiple recipients are defined in Sms it won't work ? check with Vonage API
        response = client.send_message(sms)
        self._handle_errors(response)
        return response

    def queue(self, notifiable, notification):
        """Used to queue the SMS notification to be send."""
        sms = self.build(notifiable, notification)
        client = self.get_sms_client()
        self.application.make("queue").push(client.send_message, args=(sms,))

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
