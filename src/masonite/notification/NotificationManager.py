"""Notification handler class"""
import uuid
from masoniteorm.models import Model

from ..utils.collections import Collection
from ..drivers.notification.BaseDriver import BaseDriver
from ..exceptions.exceptions import NotificationException, DriverNotFound
from ..queues import ShouldQueue


class NotificationManager(object):
    """Notification handler which handle sending/queuing notifications anonymously
    or to notifiables through different channels."""

    called_notifications = []

    def __init__(self, application, driver_config=None):
        self.application = application
        self.drivers = {}
        self.driver_config = driver_config or {}
        self.options = {"dry": False}

    def add_driver(self, name, driver):
        self.drivers.update({name: driver})

    def get_driver(self, name):
        return self.drivers[name]

    def set_configuration(self, config):
        self.driver_config = config
        return self

    def get_config_options(self, driver):
        return self.driver_config.get(driver, {})

    def send(
        self, notifiables, notification, channels=[], dry=False, fail_silently=False
    ):
        """Send the given notification to the given notifiables immediately."""
        notifiables = self._format_notifiables(notifiables)
        for notifiable in notifiables:
            # get channels for this notification
            # allow override of channels list at send
            _channels = channels if channels else notification.via(notifiable)
            _channels = self.prepare_channels(_channels)
            if not _channels:
                raise NotificationException(
                    "No channels have been defined in via() method of {0} class.".format(
                        notification.type()
                    )
                )
            for channel in _channels:
                from .AnonymousNotifiable import AnonymousNotifiable

                if (
                    isinstance(notifiable, AnonymousNotifiable)
                    and channel == "database"
                ):
                    # this case is not possible but that should not stop other channels to be used
                    continue
                notification_id = uuid.uuid4()
                self.send_or_queue(
                    notifiable,
                    notification,
                    notification_id,
                    channel,
                    dry=dry,
                    fail_silently=fail_silently,
                )

    def is_custom_channel(self, channel):
        return issubclass(channel, BaseDriver)

    def send_or_queue(
        self,
        notifiable,
        notification,
        notification_id,
        channel_instance,
        dry=False,
        fail_silently=False,
    ):
        """Send or queue the given notification through the given channel to one notifiable."""
        if not notification.id:
            notification.id = notification_id
        if not notification.should_send or dry:
            return
        try:
            # TODO: adapt with
            # self.get_driver(driver).set_options(self.options).send()
            if isinstance(notification, ShouldQueue):
                return channel_instance.queue(notifiable, notification)
            else:
                return channel_instance.send(notifiable, notification)
        except Exception as e:
            if notification.ignore_errors or fail_silently:
                pass
            else:
                raise e

        # TODO (later): dispatch send event

    def _format_notifiables(self, notifiables):
        if isinstance(notifiables, list) or isinstance(notifiables, Collection):
            return notifiables
        else:
            return [notifiables]

    def prepare_channels(self, channels):
        """Check channels list to get a list of channels string name which
        will be fetched from container later and also checks if custom notifications
        classes are provided.

        For custom notifications check that the class implements NotificationContract.
        For driver notifications (official or not) check that the driver exists in the container.
        """
        _channels = []
        for channel in channels:
            if isinstance(channel, str):
                # check that related notification driver is known and registered in the container
                try:
                    _channels.append(
                        self.application.make("notification").get_driver(channel)
                    )
                except DriverNotFound:
                    raise NotificationException(
                        "{0} notification driver has not been found in the container. Check that it is registered correctly.".format(
                            channel
                        )
                    )
            elif self.is_custom_channel(channel):
                _channels.append(channel())
            else:
                raise NotificationException(
                    "{0} notification class cannot be used because it does not implements NotificationContract.".format(
                        channel
                    )
                )

        return _channels

    def route(self, channel, route):
        """Specify how to send a notification to an anonymous notifiable."""
        from .AnonymousNotifiable import AnonymousNotifiable

        return AnonymousNotifiable().route(channel, route)
