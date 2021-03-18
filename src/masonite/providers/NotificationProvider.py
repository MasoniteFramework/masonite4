from .Provider import Provider
from ..utils.structures import load
from ..drivers.notification import (
    DatabaseDriver,
    MailDriver,
    SlackDriver,
    VonageDriver,
    # BroadcastDriver,
)
from ..notification import NotificationManager
from ..notification import MockNotification


class NotificationProvider(Provider):
    """Notifications Provider"""

    def __init__(self, application):
        self.application = application

    def register(self):
        notification_manager = NotificationManager(self.application).set_configuration(
            load(self.application.make("config.notification"))
        )
        notification_manager.add_driver("mail", MailDriver(self.application))
        notification_manager.add_driver("vonage", VonageDriver(self.application))
        notification_manager.add_driver("slack", SlackDriver(self.application))
        notification_manager.add_driver("database", DatabaseDriver(self.application))
        # notification_manager.add_driver("broadcast", BroadcastDriver(self.application))

        self.application.bind("notification", notification_manager)
        self.application.bind("mock.notification", MockNotification)
