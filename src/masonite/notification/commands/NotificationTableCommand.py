"""Notification Table Command."""
from cleo import Command
import os
import pathlib

from ...utils.filesystem import make_directory
from ...utils.time import migration_timestamp


class NotificationTableCommand(Command):
    """
    Creates the notifications table needed for storing notifications in the database.

    notification:table
        {--d|--directory=database/migrations : Specifies the directory to create the migration in}
    """

    def handle(self):
        with open(
            os.path.join(
                pathlib.Path(__file__).parent.absolute(),
                "../",
                "stubs/notification/create_notifications_table.py",
            )
        ) as fp:
            output = fp.read()

        file_name = f"{migration_timestamp()}_create_notifications_table.py"

        path = os.path.join(os.getcwd(), self.option("directory"), file_name)
        make_directory(path)

        with open(path, "w") as fp:
            fp.write(output)

        self.info(f"Migration file created: {file_name}")
