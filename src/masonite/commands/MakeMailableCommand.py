"""New Key Command."""
from cleo import Command
import inflection
import os

from ..utils.filesystem import make_directory, render_stub_file, get_module_dir


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

        filename = os.path.join(
            self.app.make("mailables.location").replace(".", "/"), name + ".py"
        )

        make_directory(filename)

        with open(filename, "w") as f:
            f.write(content)
        self.info(f"Mailable Created ({filename})")

    def get_template_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../stubs/templates/")

    def get_mailables_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../stubs/mailable/Mailable.py")
