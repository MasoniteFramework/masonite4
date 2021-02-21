"""Mail driver Class."""

from ...exceptions.exceptions import NotificationException
from .BaseDriver import BaseDriver


class MailDriver(BaseDriver):
    def __init__(self, application):
        self.application = application
        self.options = {}

    def set_options(self, options):
        self.options = options
        return self

    def send(self, notifiable, notification):
        """Used to send the email."""
        # return method(*method_args)
        mailable = self.get_data("mail", notifiable, notification)
        # check that if no _to has been defined specify it
        if not mailable._to:
            recipients = self.get_recipients(notifiable, notification)
            mailable = mailable.to(recipients)
        # TODO: allow changing driver how ?????
        return self.application.make("mail").mailable(mailable).send(driver="terminal")

    def queue(self, notifiable, notification):
        """Used to queue the email to send."""
        # return method(*method_args)
        mailable = self.get_data("mail", notifiable, notification)
        # check that if no _to has been defined specify it
        if not mailable._to:
            recipients = self.get_recipients(notifiable, notification)
            mailable = mailable.to(recipients)
        # TODO: allow changing driver
        return self.application.make("queue").push(
            self.application.make("mail").mailable(mailable).send, driver="async"
        )

    def get_recipients(self, notifiable, notification):
        """Get recipients which can be defined through notifiable route method.
        return email
        return {email: name}
        return [email1, email2]
        return [{email1: ''}, {email2: name2}]
        """
        # TODO: use Recipient from M4
        recipients = notifiable.route_notification_for("mail", notification)
        # multiple recipients
        if isinstance(recipients, list):
            _recipients = []
            for recipient in recipients:
                _recipients.append(self._format_address(recipient))
        else:
            _recipients = [self._format_address(recipients)]
        return _recipients

    def _format_address(self, recipient):
        if isinstance(recipient, str):
            return recipient
        elif isinstance(recipient, tuple):
            if len(recipient) != 2 or not recipient[1]:
                raise NotificationException(
                    "route_notification_for_mail() should return a string or a tuple (email, name)"
                )
            return "{1} <{0}>".format(*recipient)
