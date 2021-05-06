from .response_handler import response_handler
from cleo import Application as CommandApplication
from ..commands import TinkerCommand, CommandCapsule
from ..storage import StorageCapsule
import os
from ..middleware import (
    MiddlewareCapsule,
    VerifyCsrfToken,
    SessionMiddleware,
    EncryptCookies,
)
from ..routes import Router, Route
import pydoc
from ..utils.structures import load_routes


class HttpKernel:

    http_middleware = []
    route_middleware = {"web": [EncryptCookies, SessionMiddleware, VerifyCsrfToken]}

    def __init__(self, app):
        self.application = app

    def register(self):
        self.register_routes()
        self.register_middleware()

    def register_middleware(self):
        self.application.bind("middleware", MiddlewareCapsule())

    def register_routes(self):
        Route.set_controller_module_location(
            self.application.make("controller.location")
        )

        self.application.bind(
            "router",
            Router(
                Route.group(
                    load_routes(self.application.make("routes.web")), middleware="web"
                ),
            ),
        )
