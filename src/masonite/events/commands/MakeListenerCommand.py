"""New Key Command."""
from cleo import Command
from ...utils.filesystem import make_directory
import inflection
import os


class MakeListenerCommand(Command):
    """
    Creates a new listener class.

    listener
        {name : Name of the listener}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))

        with open(self.get_path(), "r") as f:
            content = f.read()
            content = content.replace("__class__", name)

        file_name = os.path.join(
            self.app.make("listeners.location").replace(".", "/"), name + ".py"
        )

        make_directory(file_name)

        with open(file_name, "w") as f:
            f.write(content)
        self.info(f"Listener Created ({file_name})")

    def get_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../../stubs/events/listener.py")
