from .Provider import Provider
from ..utils.structures import load
from ..drivers.notification import (
    MailDriver,
    VonageDriver,
    # BroadcastDriver,
    # DatabaseDriver,
    # SlackDriver,
)
from ..notification import NotificationManager


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
        # notification_manager.add_driver("database", DatabaseDriver(self.application))
        # notification_manager.add_driver("slack", SlackDriver(self.application))
        # notification_manager.add_driver("broadcast", BroadcastDriver(self.application))
        # TODO: to rewrite
        # self.app.bind("NotificationCommand", NotificationCommand())
        self.application.bind("notification", notification_manager)

    def boot(self):
        # TODO: to rewrite
        # migration_path = os.path.join(os.path.dirname(__file__), "../migrations")
        # config_path = os.path.join(os.path.dirname(__file__), "../config")
        # self.publishes(
        #     {os.path.join(config_path, "notifications.py"): "config/notifications.py"},
        #     tag="config",
        # )
        # self.publishes_migrations(
        #     [
        #         os.path.join(migration_path, "create_notifications_table.py"),
        #     ],
        # )
        pass
