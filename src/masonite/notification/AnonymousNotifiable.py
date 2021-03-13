"""Anonymous Notifiable mixin"""

from .Notifiable import Notifiable


class AnonymousNotifiable(Notifiable):
    """Anonymous notifiable allowing to send notification without having
    a notifiable entity."""

    def __init__(self):
        self._routes = {}

    def route(self, channel, route):
        """Add routing information to the target."""
        if channel == "database":
            raise ValueError(
                "The database channel does not support on-demand notifications."
            )
        self._routes[channel] = route
        return self

    def route_notification_for(self, channel):
        try:
            return self._routes[channel]
        except KeyError:
            raise ValueError(
                "Routing has not been defined for the channel {}".format(channel)
            )

    def send(self, notification, dry=False, fail_silently=False):
        """Send the given notification."""
        from wsgi import application

        return application.make("notification").send(
            self, notification, self._routes, dry, fail_silently
        )
