"""New Provider Command."""
from cleo import Command
import inflection
import os

from ..utils.filesystem import make_directory, render_stub_file, get_module_dir
from ..utils.str import dotted_to_path
from ..utils.location import base_path


class MakeProviderCommand(Command):
    """
    Creates a new mailable class.

    provider
        {name : Name of the mailable}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))

        content = render_stub_file(self.get_providers_path(), name)

        relative_filename = os.path.join(
            dotted_to_path(self.app.make("providers.location")), name + ".py"
        )
        filepath = base_path(relative_filename)
        make_directory(filepath)

        with open(filepath, "w") as f:
            f.write(content)
        self.info(f"Provider Created ({relative_filename})")

    def get_providers_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/providers/Provider.py")
