"""New Key Command."""
from cleo import Command
from ..utils.filesystem import make_directory
import inflection
import os


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

        with open(self.get_mailables_path(), "r") as f:
            content = f.read()
            content = content.replace("__class__", name)

        file_name = os.path.join(
            self.app.make("mailables.location").replace(".", "/"), name + ".py"
        )

        make_directory(file_name)

        with open(file_name, "w") as f:
            f.write(content)
        self.info(f"Mailable Created ({file_name})")

    def get_template_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../stubs/templates/")

    def get_mailables_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../stubs/mailable/Mailable.py")
