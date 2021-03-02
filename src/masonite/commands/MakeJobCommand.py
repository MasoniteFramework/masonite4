"""New Key Command."""
from cleo import Command
from ..utils.filesystem import make_directory
import inflection
import os


class MakeJobCommand(Command):
    """
    Creates a new job class.

    job
        {name : Name of the job}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))

        with open(self.get_jobs_path(), "r") as f:
            content = f.read()
            content = content.replace("__class__", name)

        file_name = os.path.join(
            self.app.make("jobs.location").replace(".", "/"), name + ".py"
        )

        make_directory(file_name)

        with open(file_name, "w") as f:
            f.write(content)
        self.info(f"Job Created ({file_name})")

    def get_template_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../stubs/templates/")

    def get_jobs_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../stubs/jobs/Job.py")
