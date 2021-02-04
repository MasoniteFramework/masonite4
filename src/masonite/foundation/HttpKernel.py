from .response_handler import response_handler
from cleo import Application as CommandApplication
from ..commands import TinkerCommand, CommandCapsule
from ..storage import StorageCapsule
import os
from ..middleware import MiddlewareCapsule, VerifyCsrfToken


class HttpKernel:

    http_middleware = [VerifyCsrfToken]
    route_middleware = {"web": []}

    def __init__(self, app):
        self.application = app

    def register(self):
        self.register_middleware()

    def register_middleware(self):
        middleware = MiddlewareCapsule()
        middleware.add(self.route_middleware).add(self.http_middleware)
        self.application.bind("middleware", middleware)

    def register_routes(self):
        pass
