"""New Key Command."""
from cleo import Command
from cryptography.fernet import Fernet
from distutils.dir_util import copy_tree
import inflection
import os


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

        with open(self.get_controllers_path(), "r") as f:
            content = f.read()
            content = content.replace("__class__", name)

        with open(
            os.path.join(
                self.app.make("controller.location").replace(".", "/"), name + ".py"
            ),
            "w",
        ) as f:
            f.write(content)
        self.info(f"Controller Created ({file_name})")

    def get_template_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../stubs/templates/")

    def get_controllers_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../stubs/controllers/Controller.py")
