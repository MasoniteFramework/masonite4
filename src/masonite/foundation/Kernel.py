from .response_handler import response_handler
from cleo import Application as CommandApplication
from ..commands import (
    TinkerCommand,
    CommandCapsule,
    KeyCommand,
    ServeCommand,
    QueueWorkCommand,
    QueueRetryCommand,
    QueueTableCommand,
    QueueFailedCommand,
    AuthCommand,
    MakeControllerCommand,
    MakeJobCommand,
    MakeMailableCommand,
)
from ..storage import StorageCapsule
from ..auth import Sign
import os
from ..environment import LoadEnvironment
from ..utils.structures import load
from ..middleware import MiddlewareCapsule

class Kernel:
    def __init__(self, app):
        self.application = app

    def register(self):
        self.load_environment()
        self.register_framework()
        self.register_commands()
        self.register_controllers()
        self.register_templates()

    def load_environment(self):
        LoadEnvironment()

    def register_controllers(self):
        self.application.bind("controller.location", "tests.integrations.controllers")

    def register_templates(self):
        self.application.bind("views.location", "tests/integrations/templates")

    def register_framework(self):
        self.application.set_response_handler(response_handler)
        self.application.use_storage_path(
            os.path.join(self.application.base_path, "storage")
        )
        self.application.bind("middleware", MiddlewareCapsule())
        self.application.bind("routes.web", "tests.integrations.web")
        self.application.bind("routes.api", "tests.integrations.api")

        self.application.bind("base_url", "http://localhost:8000")

    def register_commands(self):
        self.application.bind(
            "commands",
            CommandCapsule(CommandApplication("Masonite Version:", "4.0")).add(
                TinkerCommand(),
                KeyCommand(),
                ServeCommand(),
                QueueWorkCommand(self.application),
                QueueRetryCommand(self.application),
                QueueFailedCommand(),
                QueueTableCommand(),
                AuthCommand(self.application),
                MakeControllerCommand(self.application),
                MakeJobCommand(self.application),
                MakeMailableCommand(self.application),
            ),
        )
