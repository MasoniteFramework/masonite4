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
)
from ..storage import StorageCapsule
from ..auth import Sign
import os
from ..environment import LoadEnvironment
from ..utils.structures import load


class Kernel:
    def __init__(self, app):
        self.application = app

    def register(self):
        self.load_environment()
        self.set_framework_options()
        self.register_framework()
        self.register_database()
        self.register_commands()
        self.register_controllers()
        self.register_templates()
        self.register_storage()

    def load_environment(self):
        LoadEnvironment()

    def set_framework_options(self):
        self.application.bind("config.mail", "tests.integrations.config.mail")
        self.application.bind("config.session", "tests.integrations.config.session")
        self.application.bind("config.queue", "tests.integrations.config.queue")
        self.application.bind("config.database", "tests.integrations.config.database")

    def register_controllers(self):
        self.application.bind("controller.location", "tests.integrations.controllers")

    def register_templates(self):
        self.application.bind("views.location", "tests/integrations/templates")

    def register_database(self):
        from masoniteorm.query import QueryBuilder

        self.application.bind(
            "builder",
            QueryBuilder(
                connection_details=load(
                    self.application.make("config.database")
                ).DATABASES
            ),
        )

    def register_storage(self):
        storage = StorageCapsule(self.application.base_path)
        storage.add_storage_assets(
            {
                # folder          # template alias
                "tests/integrations/storage/static": "static/",
                "tests/integrations/storage/compiled": "static/",
                "tests/integrations/storage/uploads": "static/",
                "tests/integrations/storage/public": "/",
            }
        )
        self.application.bind("storage", storage)

    def register_framework(self):
        self.application.set_response_handler(response_handler)
        self.application.use_storage_path(
            os.path.join(self.application.base_path, "storage")
        )

        self.application.bind("routes.web", "tests.integrations.web.Route")
        self.application.bind(
            "sign", Sign("-RkDOqXojJIlsF_I8wWiUq_KRZ0PtGWTOZ676u5HtLg=")
        )

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
            ),
        )
