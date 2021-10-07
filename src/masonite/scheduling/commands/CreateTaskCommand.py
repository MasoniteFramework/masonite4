""" A CreateTask Command """
import os
import inflection
from cleo import Command
from os.path import exists

from ...utils.filesystem import make_directory, get_module_dir, render_stub_file
from ...utils.location import base_path


class CreateTaskCommand(Command):
    """
    Create a new task
    task
        {name : Name of the task you want to create}
        {--d|--directory=app/tasks : Specifies the directory to create the task in}
    """

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        output = render_stub_file(self.get_stub_task_path(), name)

        path = os.path.join(base_path(self.option("directory")), f"{name}.py")

        if exists(path):
            return self.line_error(f"Task already exists at: {path}", style="error")
        make_directory(path)

        with open(path, "w") as fp:
            fp.write(output)

        self.info(f"Task file created: {path}")

    def get_stub_task_path(self):
        return os.path.join(get_module_dir(__file__), "../../stubs/scheduling/task.py")
