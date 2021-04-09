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
        self.application.bind(
            "config.application", "tests.integrations.config.application"
        )
        self.application.bind("config.mail", "tests.integrations.config.mail")
        self.application.bind("config.session", "tests.integrations.config.session")
        self.application.bind("config.queue", "tests.integrations.config.queue")
        self.application.bind("config.database", "tests.integrations.config.database")
        self.application.bind("config.location", "tests/integrations/config")
        self.application.bind("config.cache", "tests.integrations.config.cache")
        self.application.bind("config.broadcast", "tests.integrations.config.broadcast")
        self.application.bind("config.auth", "tests.integrations.config.auth")
        self.application.bind(
            "config.filesystem", "tests.integrations.config.filesystem"
        )

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
        self.application.bind(
            "migrations.location", "tests/integrations/databases/migrations"
        )
        self.application.bind("seeds.location", "tests/integrations/databases/seeds")

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
        self.application.bind("storage_capsule", storage)

    def register_framework(self):
        from config.database import DB

        self.application.set_response_handler(response_handler)
        self.application.use_storage_path(
            os.path.join(self.application.base_path, "storage")
        )
        self.application.bind("routes.web", "tests.integrations.web.Route")

        key = load(self.application.make("config.application")).KEY
        self.application.bind("key", key)
        self.application.bind("sign", Sign(key))

        self.application.bind("base_url", "http://localhost:8000")
        self.application.bind("resolver", DB)
        self.application.bind("jobs.location", "tests/integrations/jobs")
        self.application.bind("mailables.location", "tests/integrations/mailables")

        from masonite.validation import Validator

        self.application.bind("validator", Validator)

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
