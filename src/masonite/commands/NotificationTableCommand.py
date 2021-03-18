"""Notification Table Command."""
from cleo import Command
from ..utils.filesystem import make_directory
import os
import pathlib
import datetime


class NotificationTableCommand(Command):
    """
    Creates the notifications table needed for storing notifications in database.

    notification:table
        {--d|--directory=database/migrations : Specifies the directory to create the migration in}
    """

    def handle(self):
        now = datetime.datetime.today()

        with open(
            os.path.join(
                pathlib.Path(__file__).parent.absolute(),
                "../",
                "stubs/notification/create_notifications_table.py",
            )
        ) as fp:
            output = fp.read()

        file_name = f"{now.strftime('%Y_%m_%d_%H%M%S')}_create_notifications_table.py"

        path = os.path.join(os.getcwd(), self.option("directory"), file_name)
        make_directory(path)

        with open(path, "w") as fp:
            fp.write(output)

        self.info(f"Migration file created: {file_name}")
