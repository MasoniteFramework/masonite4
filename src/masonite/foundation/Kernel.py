from .response_handler import response_handler
from cleo import Application as CommandApplication
from ..commands import TinkerCommand, CommandCapsule
from ..storage import StorageCapsule
import os


class Kernel:
    def __init__(self, app):
        self.application = app

    def register(self):
        self.register_framework()
        self.register_commands()
        self.register_controllers()
        self.register_templates()
        self.register_storage()

    def register_controllers(self):
        print("register controllers")
        self.application.bind("controller.location", "tests.integrations.controllers")

    def register_templates(self):
        self.application.bind("views.location", "tests/integrations/templates")

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

    def register_commands(self):
        self.application.bind(
            "commands",
            CommandCapsule(
                CommandApplication("Masonite Version:", "4.0").add(TinkerCommand())
            ),
        )
