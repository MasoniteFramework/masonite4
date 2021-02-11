"""New Key Command."""
from cleo import Command
from ..utils.filesystem import make_directory
import os
import pathlib
import datetime


class QueueTableCommand(Command):
    """
    Creates the jobs table

    queue:table
        {--d|--directory=database/migrations : Specifies the database connection if using database driver}
    """

    def handle(self):
        now = datetime.datetime.today()

        print(self.option("directory"))

        with open(
            os.path.join(
                pathlib.Path(__file__).parent.absolute(),
                "../",
                "stubs/queue/create_queue_jobs_table.py",
            )
        ) as fp:
            output = fp.read()
            # output = output.replace("__MIGRATION_NAME__", camelize(name))
            # output = output.replace("__TABLE_NAME__", table)

        file_name = f"{now.strftime('%Y_%m_%d_%H%M%S')}_create_queue_jobs_table.py"

        path = os.path.join(os.getcwd(), self.option("directory"), file_name)
        make_directory(path)

        with open(path, "w") as fp:
            fp.write(output)

        self.info(f"Migration file created: {file_name}")
