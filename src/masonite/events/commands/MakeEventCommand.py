"""New Event Command."""
from cleo import Command
import inflection
import os

from ...utils.filesystem import make_directory, get_module_dir, render_stub_file
from ...utils.location import base_path
from ...utils.str import dotted_to_path


class MakeEventCommand(Command):
    """
    Creates a new event class.

    event
        {name : Name of the event}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        name = inflection.camelize(self.argument("name"))

        content = render_stub_file(self.get_stub_event_path(), name)

        relative_filename = os.path.join(
            dotted_to_path(self.app.make("events.location")), name + ".py"
        )
        filepath = base_path(relative_filename)
        make_directory(filepath)

        with open(filepath, "w") as f:
            f.write(content)
        self.info(f"Event Created ({relative_filename})")

    def get_stub_event_path(self):
        return os.path.join(get_module_dir(__file__), "../../stubs/events/Event.py")
