"""New Controller Command."""
import inflection
import os

from ..utils.location import controllers_path
from ..utils.filesystem import get_module_dir, render_stub_file
from .Command import Command


class MakeControllerCommand(Command):
    """
    Creates a new controller class.

    controller
        {name : Name of the controller}
        {--r|--resource : Create a "resource" controller with the usual CRUD methods}
        {--f|force=? : Force overriding file if already exists}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        if not name.endswith("Controller"):
            name += "Controller"

        # create a resource controller if required
        if self.option("resource"):
            stub_path = self.get_resource_controller_path()
        else:
            stub_path = self.get_basic_controller_path()

        content = render_stub_file(stub_path, name)

        filename = f"{name}.py"
        path = controllers_path(filename)
        if os.path.exists(path) and not self.option("force"):
            self.warning(
                f"{path} already exists! Run the command with -f (force) to override."
            )
            return -1

        with open(path, "w") as f:
            f.write(content)

        self.info(f"Controller Created ({controllers_path(filename, absolute=False)})")

    def get_basic_controller_path(self):
        return os.path.join(
            get_module_dir(__file__), "../stubs/controllers/Controller.py"
        )

    def get_resource_controller_path(self):
        return os.path.join(
            get_module_dir(__file__), "../stubs/controllers/ResourceController.py"
        )
