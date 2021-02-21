from abc import abstractmethod
from abc import ABC


class BaseDriver(ABC):
    @abstractmethod
    def send(self, notifiable, notification):
        """Implements sending the notification to notifiables through
        this channel."""
        raise NotImplementedError(
            "send() method must be implemented for a notification channel."
        )

    @abstractmethod
    def queue(self, notifiable, notification):
        """Implements queuing the notification to be sent later to notifiables through
        this channel."""
        raise NotImplementedError(
            "queue() method must be implemented for a notification channel."
        )

    def get_data(self, channel, notifiable, notification):
        """Get the data for the notification."""
        method_name = "to_{0}".format(channel)
        try:
            method = getattr(notification, method_name)
        except AttributeError:
            raise NotImplementedError(
                "Notification model should implement {}() method.".format(method_name)
            )
        else:
            return method(notifiable)
