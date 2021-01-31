from src.masonite.foundation import Application, response_handler
from src.masonite.providers import WSGIProvider, FrameworkProvider, RouteProvider
import os


application = Application(os.getcwd())

"""First Bind important providers needed to start the server
"""

application.register_providers(
    WSGIProvider
)

"""Bind important keys to the application
"""
application.bind(
    "controller.location", 
    "tests.integrations.controllers"
)

application.add_providers(
    FrameworkProvider,
    RouteProvider
)


