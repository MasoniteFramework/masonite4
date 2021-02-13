""" A CreateTask Command """
import os

from cleo import Command
import inflection
from ...utils.filesystem import make_directory
import os
from pathlib import Path


class CreateTaskCommand(Command):
    """
    Create a new task
    task
        {name : Name of the task you want to create}
        {--d|--directory=app/tasks : Specifies the directory to create the task in}
    """

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        with open(
            os.path.join(
                Path(__file__).parent.absolute(),
                "../../",
                "stubs/scheduling/task.py",
            )
        ) as fp:
            output = fp.read().replace("__class__", name)

        path = os.path.join(os.getcwd(), self.option("directory"), f"{name}.py")

        if Path(path).exists():
            return self.line_error(f"Task already exists at: {path}", style="error")
        make_directory(path)

        with open(path, "w") as fp:
            fp.write(output)

        self.info(f"Task file created: {path}")
