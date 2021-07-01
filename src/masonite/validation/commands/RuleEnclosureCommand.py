"""New Model Command."""
from cleo import Command
from ...utils.filesystem import make_directory, file_exists
import inflection
import os


class RuleEnclosureCommand(Command):
    """
    Creates a new rule enclosure.

    rule:enclosure
        {name : Name of the rule enclosure}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))

        with open(self.get_validation_path(), "r") as f:
            content = f.read()
            content = content.replace("__class__", name)

        file_name = os.path.join(
            self.app.make("validation.location").replace(".", "/"), name + ".py"
        )

        if file_exists(file_name):
            return self.line(f"<error>File ({file_name}) already exists</error>")

        make_directory(file_name)

        with open(file_name, "w") as f:
            f.write(content)

        self.info(f"Validation Created ({file_name})")

    def get_validation_path(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.join(current_path, "../snippets/rule_enclosure.py")
