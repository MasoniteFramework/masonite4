from .response_handler import response_handler
from cleo import Application as CommandApplication
from src.masonite.commands import TinkerCommand, CommandCapsule


class Kernel:
    def __init__(self, app):
        self.application = app

    def register(self):
        self.register_framework()
        self.register_commands()
        self.register_controllers()
        self.register_templates()

    def register_controllers(self):
        self.application.bind("controller.location", "tests.integrations.controllers")

    def register_templates(self):
        self.application.bind("views.location", "tests/integrations/templates")

    def register_framework(self):
        self.application.set_response_handler(response_handler)

    def register_commands(self):
        self.application.bind(
            "commands",
            CommandCapsule(
                CommandApplication("Masonite Version:", "4.0").add(TinkerCommand())
            ),
        )
