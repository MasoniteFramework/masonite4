"""New Notification Command"""
from cleo import Command
import inflection
import os

from ...utils.filesystem import get_module_dir, make_directory, render_stub_file
from ...utils.location import base_path
from ...utils.str import dotted_to_path


class MakeNotificationCommand(Command):
    """
    Creates a new notification class.

    notification
        {name : Name of the notification}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))

        content = render_stub_file(self.get_stub_notification_path(), name)

        relative_filename = os.path.join(
            dotted_to_path(self.app.make("notifications.location")), name + ".py"
        )
        filepath = base_path(relative_filename)
        make_directory(filepath)

        with open(filepath, "w") as f:
            f.write(content)

        self.info(f"Notification Created ({relative_filename})")

    def get_stub_notification_path(self):
        return os.path.join(
            get_module_dir(__file__), "../../stubs/notification/Notification.py"
        )
