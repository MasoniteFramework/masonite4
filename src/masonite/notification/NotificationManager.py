"""Notification handler class"""
import uuid

from ..utils.collections import Collection
from ..exceptions.exceptions import NotificationException
from ..queues import ShouldQueue
from .AnonymousNotifiable import AnonymousNotifiable


class NotificationManager(object):
    """Notification handler which handle sending/queuing notifications anonymously
    or to notifiables through different channels."""

    # those classes are use for mock => should we put them only in NotificationMock ?
    sent_notifications = {}
    dry_notifications = {}

    def __init__(self, application, driver_config=None):
        self.application = application
        self.drivers = {}
        self.driver_config = driver_config or {}
        self.options = {"dry": False}

    def add_driver(self, name, driver):
        self.drivers.update({name: driver})
        self.get_driver(name).set_options(self.get_config_options(name))

    def get_driver(self, name):
        return self.drivers[name]

    def set_configuration(self, config):
        self.driver_config = config.DRIVERS
        self.options.update({"dry": config.DRY})
        return self

    def get_config_options(self, driver):
        return self.driver_config.get(driver, {})

    def send(
        self, notifiables, notification, drivers=[], dry=False, fail_silently=False
    ):
        """Send the given notification to the given notifiables."""
        notifiables = self._format_notifiables(notifiables)
        if not notification.should_send or dry or self.options.get("dry"):
            key = notification.type()
            self.dry_notifications.update(
                {key: notifiables + self.dry_notifications.get(key, [])}
            )
            return

        for notifiable in notifiables:
            # get drivers to use for sending this notification
            drivers = drivers if drivers else notification.via(notifiable)
            if not drivers:
                raise NotificationException(
                    "No drivers have been defined in via() method of {0} notification.".format(
                        notification.type()
                    )
                )
            for driver in drivers:
                driver_instance = self.get_driver(driver)
                if isinstance(notifiable, AnonymousNotifiable) and driver == "database":
                    # this case is not possible but that should not stop other channels to be used
                    continue
                if not notification.id:
                    notification.id = uuid.uuid4()
                try:
                    if isinstance(notification, ShouldQueue):
                        return driver_instance.queue(notifiable, notification)
                    else:
                        return driver_instance.send(notifiable, notification)
                except Exception as e:
                    if not notification.ignore_errors and not fail_silently:
                        raise e

    # def is_custom_channel(self, channel):
    #     return issubclass(channel, BaseDriver)

    def _format_notifiables(self, notifiables):
        if isinstance(notifiables, (list, tuple, Collection)):
            return notifiables
        else:
            return [notifiables]

    def route(self, driver, route):
        """Specify how to send a notification to an anonymous notifiable."""
        return AnonymousNotifiable(self.application).route(driver, route)

    # TESTING
    def assertNotificationDried(self, notification_class):
        assert notification_class.__name__ in self.dry_notifications.keys()
