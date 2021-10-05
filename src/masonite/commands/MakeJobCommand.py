"""New Key Command."""
from cleo import Command
import inflection
import os

from ..utils.filesystem import make_directory, render_stub_file, get_module_dir


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
        content = render_stub_file(self.get_jobs_path(), name)

        filename = os.path.join(
            self.app.make("jobs.location").replace(".", "/"), name + ".py"
        )

        make_directory(filename)

        with open(filename, "w") as f:
            f.write(content)
        self.info(f"Job Created ({filename})")

    def get_template_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/templates/")

    def get_jobs_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/jobs/Job.py")
