import os

from src.masonite.auth import Sign
from src.masonite.foundation import response_handler
from src.masonite.storage import StorageCapsule
from src.masonite.environment import LoadEnvironment
from src.masonite.configuration import Configuration, config
from src.masonite.middleware import (
    VerifyCsrfToken,
    SessionMiddleware,
    EncryptCookies,
    LoadUserMiddleware,
)
from src.masonite.routes import Route
from src.masonite.utils.structures import load_routes


class Kernel:

    http_middleware = [EncryptCookies]
    route_middleware = {"web": [SessionMiddleware, LoadUserMiddleware, VerifyCsrfToken]}

    def __init__(self, app):
        self.application = app

    def register(self):
        self.load_environment()
        self.register_configurations()
        self.register_routes()
        self.register_middleware()
        self.register_database()
        self.register_controllers()
        self.register_templates()
        self.register_storage()

    def load_environment(self):
        LoadEnvironment()

    def register_routes(self):
        Route.set_controller_module_location(
            self.application.make("controller.location")
        )

        self.application.bind("routes.web", "tests.integrations.web")

        self.application.make("router").add(
            Route.group(
                load_routes(self.application.make("routes.web")), middleware=["web"]
            )
        )

    def register_middleware(self):
        self.application.make("middleware").add(self.route_middleware).add(
            self.http_middleware
        )

    def register_configurations(self):
        # load configuration
        self.application.bind("config.location", "config")
        configuration = Configuration(self.application)
        configuration.load()
        self.application.bind("config", configuration)
        key = config("application.key")
        self.application.bind("key", key)
        self.application.bind("sign", Sign(key))

        # set locations
        self.application.bind("controller.location", "tests.integrations.controllers")
        self.application.bind("jobs.location", "tests/integrations/jobs")
        self.application.bind("mailables.location", "tests/integrations/mailables")

        self.application.bind(
            "server.runner", "src.masonite.commands.ServeCommand.main"
        )

    def register_templates(self):
        self.application.bind("views.location", "tests/integrations/templates")

    def register_database(self):
        from masoniteorm.query import QueryBuilder
        from config.database import DB

        self.application.bind(
            "builder",
            QueryBuilder(connection_details=config("database.databases")),
        )

        self.application.bind(
            "migrations.location", "tests/integrations/databases/migrations"
        )
        self.application.bind("seeds.location", "tests/integrations/databases/seeds")

        self.application.bind("resolver", DB)

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

        self.application.set_response_handler(response_handler)
        self.application.use_storage_path(
            os.path.join(self.application.base_path, "storage")
        )
