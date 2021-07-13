"""New Key Command."""
from cleo import Command
from ..utils.filesystem import make_directory
import os
import pathlib
import datetime


class QueueFailedCommand(Command):
    """
    Creates a failed jobs table

    queue:failed
        {--d|--directory=databases/migrations : Specifies the directory to create the migration in}
    """

    def handle(self):
        now = datetime.datetime.today()

        with open(
            os.path.join(
                pathlib.Path(__file__).parent.absolute(),
                "../",
                "stubs/queue/create_failed_jobs_table.py",
            )
        ) as fp:
            output = fp.read()
            # output = output.replace("__MIGRATION_NAME__", camelize(name))
            # output = output.replace("__TABLE_NAME__", table)

        file_name = f"{now.strftime('%Y_%m_%d_%H%M%S')}_create_failed_jobs_table.py"

        path = os.path.join(os.getcwd(), self.option("directory"), file_name)
        make_directory(path)

        with open(path, "w") as fp:
            fp.write(output)

        self.info(f"Migration file created: {file_name}")
