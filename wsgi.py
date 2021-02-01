from src.masonite.foundation import Application, response_handler
from src.masonite.providers import WSGIProvider, FrameworkProvider, RouteProvider, ViewProvider
import os


application = Application(os.getcwd())

"""First Bind important providers needed to start the server
"""

application.register_providers(
    WSGIProvider
)

"""Bind important keys to the application. TODO: make this all bound maybe in a new Kernel class
"""
application.bind(
    "controller.location", 
    "tests.integrations.controllers"
)

application.bind(
    "views.location", 
    "tests/integrations/templates"
)

application.add_providers(
    FrameworkProvider,
    RouteProvider,
    ViewProvider
)


