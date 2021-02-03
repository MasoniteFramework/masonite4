from .response_handler import response_handler
from cleo import Application as CommandApplication
from ..commands import TinkerCommand, CommandCapsule
from ..storage import StorageCapsule
import os


class HttpKernel:
    def __init__(self, app):
        self.application = app

    def register(self):
        pass

    #    Route Middleware
    #    HTTP Middleware

    def register_middleware(self):
        self.application.bind(
            "middleware.route",
        )
