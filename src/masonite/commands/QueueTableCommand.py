"""New Key Command."""
from cleo import Command
import os
import pathlib

from ..utils.filesystem import make_directory
from ..utils.time import migration_timestamp


class QueueTableCommand(Command):
    """
    Creates the jobs table

    queue:table
        {--d|--directory=databases/migrations : Specifies the directory to create the migration in}
    """

    def handle(self):
        with open(
            os.path.join(
                pathlib.Path(__file__).parent.absolute(),
                "../",
                "stubs/queue/create_queue_jobs_table.py",
            )
        ) as fp:
            output = fp.read()

        file_name = f"{migration_timestamp()}_create_queue_jobs_table.py"

        path = os.path.join(os.getcwd(), self.option("directory"), file_name)
        make_directory(path)

        with open(path, "w") as fp:
            fp.write(output)

        self.info(f"Migration file created: {file_name}")
