"""New Key Command."""
from cleo import Command
import os
import pathlib

from ..utils.filesystem import make_directory, get_module_dir
from ..utils.time import migration_timestamp
from ..utils.location import base_path


class QueueTableCommand(Command):
    """
    Creates the jobs table

    queue:table
        {--d|--directory=databases/migrations : Specifies the directory to create the migration in}
    """

    def handle(self):
        with open(
            os.path.join(
                get_module_dir(__file__), "stubs/queue/create_queue_jobs_table.py"
            )
        ) as fp:
            output = fp.read()

        filename = f"{migration_timestamp()}_create_queue_jobs_table.py"
        path = os.path.join(base_path(self.option("directory")), filename)
        make_directory(path)

        with open(path, "w") as fp:
            fp.write(output)

        self.info(f"Migration file created: {filename}")
