"""New Key Command."""
from cleo import Command
from cryptography.fernet import Fernet
from distutils.dir_util import copy_tree
from ..utils.filesystem import make_directory
import inflection
import os


class MakeResourceCommand(Command):
    """
    Creates a new resource class.

    resource
        {name : Name of the resource}
        {--m|--model=None : Name of the model}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        if self.option("model") == "None":
            model = None
        else:
            model = inflection.camelize(self.option("model") or "")
        if not name.endswith("Resource"):
            name += "Resource"

        with open(self.get_resources_path(), "r") as f:
            content = f.read()
            content = content.replace("__class__", name)
            content = content.replace("__model__", model or self.argument("name"))
            content = content.replace("__record__", inflection.underscore(model or self.argument("name")))

        file_name = os.path.join(
                self.app.make("resource.location").replace(".", "/"), name + ".py"
            )
        make_directory(file_name)
        with open(
            file_name,
            "w",
        ) as f:
            f.write(content)
        self.info(f"Resource Created ({file_name})")

    def get_resources_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../stubs/api/Resource.py")
