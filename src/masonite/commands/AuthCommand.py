"""Scaffold Auth Command."""
from cleo import Command
from distutils.dir_util import copy_tree
import os

from ..utils.location import controllers_path, views_path
from ..utils.filesystem import get_module_dir


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
            views_path("auth"),
        )
        copy_tree(self.get_controllers_path(), controllers_path("auth"))

    def get_template_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/templates/auth")

    def get_controllers_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/controllers/auth")
