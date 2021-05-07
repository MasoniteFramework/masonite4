from src.masonite.foundation import response_handler
from cleo import Application as CommandApplication
from src.masonite.storage import StorageCapsule
from src.masonite.auth import Sign
import os
from src.masonite.environment import LoadEnvironment
from src.masonite.utils.structures import load
from src.masonite.middleware import (
    MiddlewareCapsule,
    VerifyCsrfToken,
    SessionMiddleware,
    EncryptCookies,
)
from src.masonite.tests.HttpTestResponse import HttpTestResponse
from src.masonite.tests.TestResponseCapsule import TestResponseCapsule
from src.masonite.routes import Route
from src.masonite.utils.structures import load_routes


class Kernel:

    http_middleware = []
    route_middleware = {"web": [EncryptCookies, SessionMiddleware, VerifyCsrfToken]}

    def __init__(self, app):
        self.application = app

    def register(self):
        # Register routes
        self.load_environment()
        self.register_configurations()
        self.register_routes()
        self.register_middleware()
        self.register_database()
        self.register_controllers()
        self.register_templates()
        self.register_storage()
        self.register_testing()

    def load_environment(self):
        LoadEnvironment()

    def register_routes(self):
        Route.set_controller_module_location(
            self.application.make("controller.location")
        )

        self.application.bind("routes.web", "tests.integrations.web")

        self.application.make("router").add(
            Route.group(
                load_routes(self.application.make("routes.web")), middleware="web"
            )
        )

    def register_middleware(self):
        self.application.make("middleware").add(self.route_middleware).add(
            self.http_middleware
        )

    def register_configurations(self):
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

        self.application.bind("base_url", "http://localhost:8000")

        self.application.bind("jobs.location", "tests/integrations/jobs")
        self.application.bind("mailables.location", "tests/integrations/mailables")
        self.application.bind(
            "server.runner", "src.masonite.commands.ServeCommand.main"
        )

        key = load(self.application.make("config.application")).KEY
        self.application.bind("key", key)
        self.application.bind("sign", Sign(key))

    def register_controllers(self):
        self.application.bind("controller.location", "tests.integrations.controllers")

    def register_templates(self):
        self.application.bind("views.location", "tests/integrations/templates")

    def register_storage(self):
        storage = StorageCapsule(self.application.base_path)
        storage.add_storage_assets(
            {
                # folder                             # template alias
                "tests/integrations/storage/static": "static/",
                "tests/integrations/storage/compiled": "static/",
                "tests/integrations/storage/uploads": "static/",
                "tests/integrations/storage/public": "/",
            }
        )
        self.application.bind("storage_capsule", storage)

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

        from config.database import DB

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

    def register_testing(self):
        test_response = TestResponseCapsule(HttpTestResponse)
        self.application.bind("tests.response", test_response)
