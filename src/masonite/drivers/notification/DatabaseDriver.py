"""Database notification driver."""
import json

from ...notification import DatabaseNotification
from .BaseDriver import BaseDriver


class DatabaseDriver(BaseDriver):
    def __init__(self, application):
        self.application = application
        self.options = {}

    def set_options(self, options):
        self.options = options
        return self

    def send(self, notifiable, notification):
        """Used to send the email and run the logic for sending emails."""
        data = self.build(notifiable, notification)
        return DatabaseNotification.create(data)

    def queue(self, notifiable, notification):
        """Used to queue the database notification creation."""
        data = self.build(notifiable, notification)
        return self.application.make("queue").push(
            DatabaseNotification.create, args=(data,)
        )

    def build(self, notifiable, notification):
        """Build an array payload for the DatabaseNotification Model."""
        return {
            "id": str(notification.id),
            "type": notification.type(),
            "notifiable_id": notifiable.id,
            "notifiable_type": notifiable.get_table_name(),
            "data": json.dumps(self.get_data("database", notifiable, notification)),
            "read_at": None,
        }
