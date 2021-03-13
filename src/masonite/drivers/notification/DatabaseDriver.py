"""Database driver Class."""
import json
from masonite import Queue

from ..models import DatabaseNotification
from .BaseDriver import BaseDriver


class DatabaseDriver(BaseDriver):
    def __init__(self, application):
        self.application = application
        self.options = {}

    def send(self, notifiable, notification):
        """Used to send the email and run the logic for sending emails."""
        model_data = self.build_payload(notifiable, notification)
        return DatabaseNotification.create(model_data)

    def queue(self, notifiable, notification):
        """Used to queue the database notification creation."""
        model_data = self.build_payload(notifiable, notification)
        return self.app.make(Queue).push(
            DatabaseNotification.create, args=(model_data,)
        )

    def serialize_data(self, data):
        return json.dumps(data)

    def build_payload(self, notifiable, notification):
        """Build an array payload for the DatabaseNotification Model."""
        return {
            "id": str(notification.id),
            "type": notification.type(),
            "notifiable_id": notifiable.id,
            "notifiable_type": notifiable.get_table_name(),
            "data": self.serialize_data(
                self.get_data("database", notifiable, notification)
            ),
            "read_at": None,
        }
