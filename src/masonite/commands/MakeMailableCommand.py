"""New Mailable Command."""
from cleo import Command
import inflection
import os

from ..utils.filesystem import make_directory, render_stub_file, get_module_dir
from ..utils.str import as_filepath
from ..utils.location import base_path


class MakeMailableCommand(Command):
    """
    Creates a new mailable class.

    mailable
        {name : Name of the mailable}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))
        content = render_stub_file(self.get_mailables_path(), name)

        relative_filename = os.path.join(
            as_filepath(self.app.make("mailables.location")), name + ".py"
        )
        filepath = base_path(relative_filename)
        make_directory(filepath)

        with open(filepath, "w") as f:
            f.write(content)

        self.info(f"Mailable Created ({relative_filename})")

    def get_mailables_path(self):
        return os.path.join(get_module_dir(__file__), "../stubs/mailable/Mailable.py")
