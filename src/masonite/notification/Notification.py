"""Base Notification facade."""


class Notification:
    """Notification class representing a notification."""

    def __init__(self, *args, **kwargs):
        self.id = None
        self._dry = False
        self._fail_silently = False

    def broadcast_on(self):
        """Get the channels the event should broadcast on."""
        return []

    def via(self, notifiable):
        """Defines the notification's delivery channels."""
        raise NotImplementedError("via() method should be implemented.")

    @property
    def should_send(self):
        return not self._dry

    @property
    def ignore_errors(self):
        return self._fail_silently

    @classmethod
    def type(cls):
        """Get notification type defined with class name."""
        return cls.__name__

    def dry(self):
        """Sets whether the notification should be sent or not.

        Returns:
            self
        """
        self._dry = True
        return self

    def fail_silently(self):
        """Sets whether the notification can fail silently (without raising exceptions).

        Returns:
            self
        """
        self._fail_silently = True
        return self
