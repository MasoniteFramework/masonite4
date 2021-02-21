"""Notifiable mixin"""
from masoniteorm.relationships import has_many

from .DatabaseNotification import DatabaseNotification
from ..exceptions.exceptions import NotificationException


class Notifiable(object):
    def notify(self, notification, channels=[], dry=False, fail_silently=False):
        """Send the given notification."""
        from wsgi import application

        return application.make("notification").send(
            self, notification, channels, dry, fail_silently
        )

    def route_notification_for(self, channel):
        """Get the notification routing information for the given channel."""
        # check if routing has been specified on the model
        method_name = "route_notification_for_{0}".format(channel)

        try:
            method = getattr(self, method_name)
            return method(self)
        except AttributeError:
            # if no method is defined on notifiable use default
            if channel == "database":
                # with database channel, notifications are saved to database
                pass
            elif channel == "mail":
                return self.email
            else:
                raise NotificationException(
                    "Notifiable model does not implement {}".format(method_name)
                )

    @has_many("id", "notifiable_id")
    def notifications(self):
        return DatabaseNotification.where("notifiable_type", "users").order_by(
            "created_at", direction="DESC"
        )

    @property
    def unread_notifications(self):
        """Get the entity's unread notifications. Only for 'database'
        notifications."""
        return self.notifications.where("read_at", "==", None)

    @property
    def read_notifications(self):
        """Get the entity's read notifications. Only for 'database'
        notifications."""
        return self.notifications.where("read_at", "!=", None)
