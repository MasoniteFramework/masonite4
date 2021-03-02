"""New Key Command."""
from cleo import Command
from cryptography.fernet import Fernet
from distutils.dir_util import copy_tree
import os


class AuthCommand(Command):
    """
    Creates a new authentication scaffold.

    auth
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        copy_tree(
            self.get_template_path(),
            os.path.join(self.app.make("views.location").replace(".", "/"), "auth"),
        )
        copy_tree(
            self.get_controllers_path(),
            os.path.join(
                self.app.make("controller.location").replace(".", "/"), "auth"
            ),
        )

    def get_template_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../stubs/templates/auth")

    def get_controllers_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../stubs/controllers/auth")
