"""New Key Command."""
from cleo import Command
import inflection
import os

from ..utils.location import controller_path
from ..utils.filesystem import get_module_dir, render_stub_file


class MakeControllerCommand(Command):
    """
    Creates a new controller class.

    controller
        {name : Name of the controller}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        if not name.endswith("Controller"):
            name += "Controller"

        content = render_stub_file(self.get_controllers_path(), name)

        filename = name + ".py"
        with open(controller_path(filename), "w") as f:
            f.write(content)

        self.info(f"Controller Created ({filename})")

    def get_template_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/templates/")

    def get_controllers_path(self):
        return os.path.join(
            get_module_dir(__file__), "../stubs/controllers/Controller.py"
        )
